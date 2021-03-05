# Streaming Data Pipeline

This repository contains a working docker-compose stack which contains a working end-to-end scalable streaming data pipeline using generic, non-saas components which could be used for a variety of purposes.

This work was undertaken to fulfil an assigned technical take-home assessment for a Senior Python/Data Back-End Dev position. The purpose of this pipeline is to process messy data, tying unstructured data to known entities in order to produce metrics. In this approach, I stay within the brief's constraints and produce a horizontally-scalable solution using performant NLP techniques to match menu item text to products.

I have provided a brief self-evaluation against the brief in further sections.

Within this stack there are a few containers:

Pipeline

- A Flask API handling CSV POSTed input files
- A Kafka instance proctoring a subscribable topic for individual rows
- Faust worker instances to consume from the Kafka topic
- A PostgreSQL database to store results

Infrastructure

- A Zookeeper instance to manage Kafka workers
- A Kafdrop instance to monitor Kafka topics via a web-app
- A PgAdmin instance to view and monitor the endpoint database

![Alt text](/doc/images/Planning.jpg?raw=true "Whiteboard showing the initial system architecture plan")
Whiteboard showing the initial system architecture plan

![Alt text](/doc/images/Kafdrop.png?raw=true "Kafdrop showing the eventual ingestion topic")
Kafdrop showing the eventual ingestion topic

![Alt text](/doc/images/Debug.png?raw=true "Faust workers processing the ingestion Kafka topic")
Faust workers processing the ingestion Kafka topic

![Alt text](/doc/images/Pgadmin.png?raw=true "Pgadmin showing the final state of the data, correct matches in enriched form")
Pgadmin showing the final state of the data, correct matches in enriched form

## The Brief

This task was given as a take-home technical test at a Senior Developer level. The company and their data have been redacted from both the source code and testing data.

The specific requirements and constraints given are listed below.

### Data sources:

- `input.csv`: A dump of product names and descriptions entered by users on menus
- `terms.csv`: A list of brand names which may be mentioned in product names and descriptions

### Your code should demonstrate this functionality:

- Some business logic that takes the `input.csv` file as an input stream and uses stream processing to analyse each row
- Some business logic that uses a pattern matching approach of your choice to identify if a row contains term matches from the `terms.csv` (consider terms in the `input.csv` not being spelled correctly)
- A data layer that writes matches found in form of `MenuId`, `TermId` to a relational database using a write stream

### Constraints:

- Use Python
- Use a relational database of your choice to store matches
- To make your code scaleable, everything has to be streamed
- Use any frameworks and libraries of your choice
- Write unit tests
- Set yourself a time limit
- Includes notes in your code where you would like improve or extend it, if you had more time 

### Bonus task:

- Add a simple REST API that can be used to call your code by posting the `input.csv` file to it

## Self Evaluation

In this section, I self-evaluate the work undertaken with reference to the brief. In further sections I comment on further steps that should be taken to create a more production-ready system.

### Planning

I took an hour to plan the solution initially. The brief calls for some fairly specific constraints, and this informed the architecture I proposed.

![Alt text](/doc/images/Planning.jpg?raw=true "Planning")

The planning was mostly done away from the computer, referring to the brief and whiteboarding the stages data would need to go through in order to be ingested, cleaned, enriched and persisted.

You can see from the rough sketch above that my initial solution proposed an HDFS staging area for the inbound data and a NiFi instance to aid in scalable ETL before sanitised data into a queue of some sort for workers to consume.

I felt that the original sketch represented a more production-ready system but given a rough self-imposed time-limit of 2 working days, I think this would have added needless complexity given that robustness is not going to be a major issue.

I stated a few ideas for things like the web server and RDBMS, settling on Flask (for simplicity) and PostgreSQL (pseudo object-store) respectively. For workers, I considered home-rolling Kafka consumers using Celery but again felt this would be needlessly complex for the purposes of the demo system.

### Time

I gave myself about 2 working days to complete this task, and eventually clocked in at around 16 hours. This information was captured using Toggl.

The tasks below are aggregated and only give a rough idea of the sequence of events in descending order.

| Task      | Duration |
| ----------- | ----------- |
| Database layer - Matcher data egress      | 02:23:56       |
| Database layer - Psql bootstrapping   | 01:47:12        |
| Database layer - Psql infra   | 00:44:14        |
| Docker Infra   | 03:12:41        |
| Faust consumer   | 02:22:33        |
| Flask Kafka producer   | 01:54:34        |
| Git shuffling   | 00:14:01        |
| Matching engine   | 02:32:10        |
| Planning   | 01:02:26        |
| **Total**   | **16:13:47**        |

### Domain Logic

Although this system has many threads and vertices pulling together, the main domain-job here is to take a menu item's human-readable, unstructured description and tie this to a product inventory.

To do this, within the Faust worker, there is an NLP layer to break down the unstructured text into discrete tokens, before matching these against the list of inventory terms.

In the matching logic, several steps of note are taken in order to preserve performance. The emphasis is on exiting early if we get an early hit on our term. When we have to do heavy-lifting analysis, it's as a last resort, and should happen in the C layer. The terms themselves are cached once to prevent multiple calls to the same file.

- A partial or full search is available in order to search against just the product name, or the name and the description
- Jaccard distance is used to approximate whether the terms have enough overlap to warrant further matching logic
  - As in, don't go calculating Levenshtein distance when the terms don't even share more than a percentage of the same letters
- Multi-word tokens (parts of a Proper Noun for example) are joined before matching as sets of these may represent different products 
- Don't bother with distance searching if we don't have any set-intersection in the letters of our terms
- Eventually perform Levenshtein distance-matching on the terms with a set threshold
- Extract term-product pairs into term matches which are then fed to the database as successful matches

```python
def _process_match(self, input_string, menu_item):

        term_matches = []

        point_match = lambda a, b : a.lower() in b.lower()

        for term_id, term in self.term_cache.items():

            match_found = False

            # If we have a direct match, don't do anything fancy
            if point_match(term, input_string):
                match_found = True
            # Before performing heavy NLP operations
            # Check Jaccard distance of the compared terms
            elif distance.jaccard(term, input_string) > self.jacc_threshold:
                # Now we can perform a distance search on individual linguistic tokens
                tokens = self.tokeniser.tokenize(input_string)
                for token in tokens:
                    token_text = ''
                    # If our tokeniser model returns multi-part tokens, create a string
                    if type(token) is list:
                        token_text = ' '.join([single_token.text for single_token in token])
                    else:
                        token_text = token.text
                    # Don't bother distance searching if the terms don't share any common letters
                    # This uses set intersection for performance
                    if self._terms_share_common_letters(token_text, term):
                        # Perform Levenshtein distancing search on a prefined proximity threshold
                        if self._distance_match(token_text, term):
                            match_found = True

            if match_found:
                term_matches.append((term_id, term))

        menu_item['term_matches'] = term_matches

        return menu_item
```

### Overall Fitness to the Brief

## The Good

I believe this task went well generally speaking. I managed to bootstrap infrastructure to support all parts of the application, such that with a little config tweaking it could be made to scale horizontally at all levels other than the endpoint database. I didn't put work into scaling out the database layer because I think in production I'd prefer to use a sharded database or HDFS cluster for further scalability. 

In terms of time, I stuck to my 2-day limit, clocking in at 16 hours. Going into this task I had never worked with Faust before and had little experience interfacing with Kafka, managing to hook both up in a scalable way is a fairly good achievement for the time limit.

Architecturally, in the main areas of Python code - the Flask API and the Faust Worker, I'm relatively happy with the structure. When I had a lot of time left, I took the time to introduce pseudo-interfaces and associated factories which will make extending and altering this code much easier.

In the business logic layer, I managed to create a performant NLP-based solution which produced good results and left room for extension. Leveraging lower-level APIs in C for calculating Jaccard and Levenshtein distances made good performance gains in heavy-lifting areas.

The actual docker stack itself uses overrides for environments so that one could run this on Windows easily and extendable builds for off-the-shelf images so that these can be altered easily. 

### Complete:

- Use Python
- Use a relational database of your choice to store matches
- To make your code scaleable, everything has to be streamed
- Use any frameworks and libraries of your choice
- Set yourself a time limit
- Includes notes in your code where you would like improve or extend it, if you had more time 

## The Bad

Even though I met the brief's specificities within the time limit, I missed the mark in one area. The brief specifically requests unit tests to be written, which I left until the end. In doing so, I didn't manage to integrate any tests for this work. I essentially planned to write behavioural/integration tests in the last phase to simply run the pipeline and make sure the data was processed correctly, but have decided to not fudge this and stick with the time limit.

It's not that testing this is difficult, but given the amount of work in making this work scalably in just 2 days, I think if I had to incorporate unit tests to any useful degree would have taken at least a half day from the project. I could consider this a failing on my part, but honestly I was very set on delivering a working solution which met the technical criteria and would scale well.

Given that I took on the bonus task of running up an API layer for the pipeline, maybe I could have used this time to instead write some unit tests around the NLP logic or something like that.

### Incomplete:

- Write unit tests

## Further Work (A.K.A The TODO Epitaph)

Resisting the temptation to keep working on this, it's more useful to keep the state of the application in-place as it was at the end of the technical test.

Given that Parkinson's Law states that *work expands to fill the time alloted*, if I had 2 weeks to spend on this instead of 2 days, I'd have produced something better, but presumably this would still have achieved the same goal. In this sense, having a shallow time limit was quite fun.

On this note, there are *a lot* of things I'd like to expand upon and remediate in this codebase, if I had more time:

- Include unit tests in the API logic layer, and the Faust worker's NLP layer.
  - Include some behavioural/integration tests to test the end-to-end logic for matching
- Increase *robustness* in all areas
  - Validation
  - Exception handling
- General security hardening with respect to ports etc.
- Create some documentation for the system 
- Tidy the passthrough of certain config variables to the docker components for *dev* and *prod* respectively
  - Tidy up env files for ports etc. in a sane way
- Introduce HDFS cluster and NiFi or Airflow back into the mix to handle intermediary steps
- Split NLP code into own module, build into artefact and place in docker image
- Break down API layer further
  - Consider moving file streamer itself into a microservice or handle via NiFi etc.
- Consider moving to K8s for production-grade scaling
  - Consider building distroless containers
  - Consider using Terraform to run up the stack so this can be moved to the cloud easily
- Consider caching product-inventory "term" lists in ElasticSearch or similar to smooth the querying of these

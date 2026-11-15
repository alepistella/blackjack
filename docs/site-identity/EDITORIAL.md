# Editorial rules / practical engineering, readable prose

## Voice

Experienced, direct, curious. Explain the interesting decision without announcing expertise. The technical detail earns attention; the writing should not demand admiration. A little dry humour can make a field note feel human, but a test report does not need a joke in every section.

Public pages default to English. Use sentence case, active verbs and connected paragraphs. Avoid em dashes, ceremonial introductions, generic conclusions, punchline slogans and repeated disclaimers. Do not make every article about avoiding an assistant's mistakes. State a relevant limitation once, near the result it qualifies.

### Before / after

**Avoid:** “Leveraging cutting-edge onboard AI, Blackjack revolutionises autonomous robotics.”

**Prefer:** “The question is whether onboard inference can share the rover's power budget with sensing and drive control.” This states an engineering question; it does not imply that the test has already passed.

**Avoid:** “This groundbreaking architecture eliminates the limitations of traditional stacks.”

**Prefer:** “This experiment tests one component boundary. The rest of the system remains part of the setup.” Name the actual component when writing the final article.

**Avoid:** “As a CTO with two decades of experience, I successfully identified...”

**Prefer:** State the problem and the observation. The bio already covers professional context.

## Homepage

Answer, in order: what is this project, what stage is it at, what question is being worked on, where can the reader inspect the work? A short bio and consistent LinkedIn/GitHub links connect the projects to their author. Link to dum-e as related work without presenting its results as Blackjack results.

Do not convert target capabilities into current capabilities. A hardware roadmap, mechanical render or design calculation is valuable in its own right when labelled accurately.

## Long study template

1. **Title:** the question or concrete mechanism, not a claim of superiority.
2. **Standfirst:** scope and reason to read, in two or three sentences at most.
3. **Status and context:** analysis, simulation, bench test or field test; author and actual publication/update dates.
4. **Question and boundary:** what is being decided; which components and dependencies are included.
5. **Method:** inputs, versions, settings, baseline, intervention, repetitions and exclusions.
6. **Evidence:** plots, images and baseline/intervention table, with units and links to raw artifacts.
7. **Interpretation:** what explains the observation; what remains an inference.
8. **Reproduce:** exact revision, configuration, commands, expected output and rollback if relevant.
9. **Limits and next check:** a concrete open question, not a generic invitation to “join the journey”.

Use only the sections the study actually needs. Five good sections are better than nine empty ones. Do not use a synthetic “result” to fill the layout.

## Short field note template

One design choice, the trigger, alternatives, decision and next verification. An annotated render or close-up can be sufficient. Link the detailed study. Keep planned checks explicitly prospective.

## Metadata

Each note needs a stable lowercase slug, title, ISO publication date, category, short summary, tags, source body, `draft` and `demo`. An optional `updated` date records a real substantive update. Dates should be factual. Never change them to imply that work happened at a different time.

Keep categories sparse and useful: Integration, Control, Perception, Power, Method. Tags describe specific components or techniques. They are not a list of recruitment keywords.

## Evidence and authorship

Every important number must be traceable. Describe whether it came from a datasheet, calculation, simulation or physical measurement. Do not change screenshot values or omit failures to make a comparison look cleaner. Do not equate a few development runs with an independent validation campaign.

Use “I” for actions Alessandro actually performed. A model can be credited in the method for generating weights, code, or analysing traces when that happened. Do not imply that the author chose coefficients or diagnosed a mechanism merely because they supplied the goal. No generic footer is required in every page; accurate provenance is still required where it changes how the work should be understood.

Keep third-party quotations short and linked. Paraphrase in the author's own voice. A reference is not proof of a claim outside that source's scope. Do not use a GitHub issue as an advertising billboard; contextual technical correspondence belongs elsewhere, not in this template's publishing workflow.

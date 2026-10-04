## Enterprise AI Engineering Assistant

An AI-powered codebase intelligence system for understanding and reasoning about unfamiliar software repositories.

The system combines deterministic structural analysis, semantic code retrieval, evidence assembly, and local LLM reasoning to answer repository-level developer questions using evidence from the actual codebase.

## Problem

Understanding a large software repository often requires developers to piece together information scattered across source files, functions, classes, dependencies, tests, and documentation.

Questions such as:

- How does this feature work?
- Where is this functionality implemented?
- What does this function depend on?
- Which tests cover this functionality?
- What components are involved in this workflow?
- Is there enough evidence to answer this question?

are difficult to answer reliably using an LLM alone.

An LLM may understand individual code snippets but can miss structural relationships or make unsupported assumptions about a repository.

This project explores a different approach:

> **Use deterministic code analysis to establish repository structure, semantic retrieval to identify relevant code, and an LLM to reason over the resulting evidence.**

## What Makes This Different

Traditional LLM-based code assistants can reason about code, but they may struggle to reliably understand relationships across a repository.

This system separates repository understanding into complementary components:

- **Structural analysis** determines what exists and how code elements are connected.
- **Semantic retrieval** finds code relevant to natural-language questions.
- **Evidence assembly** expands retrieved candidates using structural relationships.
- **LLM reasoning** interprets the assembled evidence and produces the final response.
- **Evidence grounding** constrains repository claims to information found in the analyzed codebase.

The goal is not to replace deterministic analysis with an LLM, but to use the LLM where interpretation is useful and deterministic analysis where exact repository structure matters.

## Example

Question:

> What does `checkout` depend on?

The system retrieves relevant code, follows structurally established relationships, assembles supporting evidence, and asks the reasoning model to produce a grounded explanation.

Example result:

```text
checkout
├── calculate_discount
└── process_payment
    └── validate_payment
```
## Core Idea

The system separates repository understanding into different responsibilities:

- **Structural analysis** determines what exists and how repository components are related.
- **Semantic retrieval** identifies code that is conceptually relevant to a developer's question.
- **Evidence assembly** combines retrieved code with structurally related information.
- **LLM reasoning** interprets the assembled evidence and produces a natural-language answer.
- **Evidence-based abstention** allows the system to state when the available repository evidence is insufficient.

The goal is not to build a generic "chat with code" application, but to investigate whether combining deterministic and probabilistic techniques can produce more grounded repository-level answers.


## Architecture

The system follows a hybrid repository-understanding pipeline that combines deterministic code analysis with semantic retrieval and LLM reasoning.

```text
                    Repository
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
    Structural Analysis      Semantic Representation
             │                     │
             ▼                     ▼
      Code Structure        Semantic Documents
      + Relationships             │
             │                     ▼
             ▼              Embedding Index
        Repository                 │
           Graph                   │
             │                     │
             └──────────┬──────────┘
                        │
                        ▼
                  User Question
                        │
                        ▼
               Semantic Retrieval
                        │
                        ▼
                Candidate Nodes
                        │
                        ▼
                Evidence Assembly
                        │
             ┌──────────┼──────────┐
             │          │          │
             ▼          ▼          ▼
          Source   Relationships  Tests
             │          │          │
             └──────────┼──────────┘
                        ▼
                 Evidence Bundle
                        │
                        ▼
                   Local LLM
                        │
                        ▼
                 Grounded Answer

```

## How It Works

Consider the developer question:

> What does `checkout` depend on?

The system processes the question through the following stages.

### 1. Analyze the Repository

The repository is analyzed before answering questions.

For the demo repository, the analyzer discovers relationships such as:

```text
create_order
    │
    ▼
checkout
    ├──► calculate_discount
    └──► process_payment
              │
              ▼
       validate_payment
```

### Evaluation

The system is evaluated using a controlled demonstration repository with known functions, dependencies, tests, and relationships.

The evaluation focuses on several dimensions rather than answer correctness alone:

- Retrieval quality
- Evidence relevance
- Answer correctness
- Grounding
- Abstention on unsupported questions

### Semantic Retrieval Evaluation

A small benchmark of repository-level questions was used to evaluate semantic candidate retrieval.

The current benchmark produced:

| Metric | Result |
|---|---:|
| Recall@1 | 0.875 |
| Recall@3 | 1.000 |
| Recall@5 | 1.000 |
| MRR | 0.917 |

These results indicate that the relevant repository entity was usually retrieved at the highest rank and was present within the top three candidates for all benchmark questions.

The benchmark is intentionally small and is used as an engineering validation of the current MVP rather than as a general claim about semantic retrieval performance.

### End-to-End Evaluation

The complete pipeline was evaluated using representative repository questions covering:

- Workflow understanding
- Implementation location
- Dependency identification
- Test identification
- Unsupported functionality

The evaluation revealed an important distinction between **answer correctness** and **evidence correctness**.

For example, the system could produce a correct dependency answer while initially relying on analyzer meta-tests as supporting evidence. This led to a targeted retrieval-boundary change that excluded analyzer infrastructure tests from the semantic index while retaining legitimate application tests.

After the change, legitimate checkout tests remained retrievable while analyzer meta-tests were excluded from the semantic candidate pool.

### Abstention

Unsupported questions are also included in the evaluation.

For example:

> Where is the email notification service implemented?

The repository does not contain such an implementation. The system correctly responds that the available repository evidence is insufficient rather than inventing a file or function.

This evaluates an important property of repository-level AI systems:

> **The system should prefer an explicit lack of evidence over an unsupported claim.**

### Evaluation Philosophy

The project treats repository understanding as an evidence-grounding problem.

Therefore, evaluation does not stop at:

> "Did the model produce the expected answer?"

It also asks:

> "Did the system retrieve the right evidence?"

and:

> "Was the answer actually supported by that evidence?"

This distinction is used to identify failures in retrieval, evidence assembly, and LLM reasoning separately.



### Performance

Performance profiling was used to identify where the MVP spent time during a typical query.

A representative run produced approximately:

| Stage | Time |
|---|---:|
| Repository analysis | 0.035 s |
| Model loading | 9.380 s |
| Semantic index loading | 0.011 s |
| Semantic retrieval | 0.667 s |
| Evidence assembly | 0.005 s |
| LLM reasoning | 59.408 s |

The exact timings vary between runs and depend on the local hardware and model state.

### Semantic Indexing

An early implementation re-encoded every semantic document whenever a question was asked.

On the CPU-only development environment, this resulted in extremely slow query processing.

The architecture was changed so that document embeddings are generated during index construction and persisted locally.

The query path now performs only:

```text
Question
   ↓
Query embedding
   ↓
Similarity against stored document embeddings
   ↓
Ranked candidates
```

### Project Structure

```text
enterprise-ai-demo-repo/
│
├── analyzer/                  # Core codebase intelligence system
│   ├── analyzer.py            # Repository-level analysis
│   ├── parser.py              # Python AST parsing
│   ├── extractor.py           # Structural fact extraction
│   ├── graph.py               # Repository graph construction and queries
│   ├── models.py              # Core data models
│   ├── semantic.py            # Semantic document construction
│   ├── semantic_index.py      # Semantic index construction and persistence
│   ├── semantic_retriever.py  # Semantic candidate retrieval
│   ├── assembly.py            # Evidence assembly
│   ├── evidence.py            # Evidence construction
│   ├── sufficiency.py         # Evidence inspection
│   ├── reasoner.py            # LLM reasoning interface
│   └── app.py                 # Application-level orchestration
│
├── app/                       # Controlled demo repository
│   ├── auth/
│   ├── discounts/
│   ├── orders/
│   └── payments/
│
├── tests/                     # Automated tests for the system
│
├── experiments/               # Experiments and engineering investigations
│
├── docs/
│   ├── architecture.md        # Demo application's architecture
│   └── demo-repository.md     # Description of the demo repository
│
├── cli.py                     # Command-line entry point
├── README.md                  # Project documentation
└── .gitignore                 # Ignored local/generated files
```

### Setup

### Requirements

The MVP currently targets:

- Python 3.10+
- A local Ollama installation
- Sufficient system memory to run the selected local language model

### 1. Clone the Repository

```bash
git clone <repository-url>
cd enterprise-ai-demo-repo
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install and Start Ollama

Install Ollama separately and make sure it is running.

Pull the reasoning model used by the MVP:

```bash
ollama pull qwen3:4b-instruct
```

### 5. Run the Tests

```bash
python -m pytest
```

### 6. Run the CLI

```bash
python cli.py "How does checkout work?"
```

The system analyzes the repository, retrieves relevant code, assembles supporting evidence, and generates a grounded answer using the local reasoning model.

The semantic index is generated automatically when it does not already exist.


## Usage

Once the environment and local reasoning model are configured, ask questions about the repository through the command-line interface.

### Example

```bash
python cli.py "How does checkout work?"
```

The system will:

1. Analyze the repository structure.
2. Retrieve semantically relevant code.
3. Expand the retrieved candidates using structural relationships.
4. Assemble source, relationship, and test evidence.
5. Provide the evidence to the local reasoning model.
6. Generate a grounded answer.

Another example:

```bash
python cli.py "What does checkout depend on?"
```

The response includes the generated answer followed by the repository evidence used to support it.

The CLI is intentionally simple for the MVP. The underlying `analyzer/` package contains the repository analysis, retrieval, evidence assembly, and reasoning components.


## Limitations

The current MVP intentionally focuses on a small, controlled scope.

### Language Support

The structural analyzer currently targets Python repositories using Python's AST.

Other programming languages are not currently supported.

### Static Analysis Limitations

The repository graph is derived from static source analysis.

Some relationships can be difficult or impossible to determine statically, including:

- Dynamic dispatch
- Complex aliasing
- Runtime-generated objects
- Reflection
- Highly dynamic imports
- Complex factory patterns
- Behavior that depends on runtime state

The analyzer therefore represents the relationships it can deterministically establish rather than claiming complete knowledge of runtime behavior.

### Repository Scale

The current semantic index uses a simple persistent local representation.

This is sufficient for the small demonstration repository used by the MVP, but larger repositories may require more scalable indexing and retrieval infrastructure.

### Evaluation Scope

The current evaluation uses a small controlled repository and a limited set of representative questions.

The reported retrieval metrics should therefore be interpreted as validation of the current implementation rather than as a general benchmark of repository-level code understanding.

### LLM Limitations

The reasoning model is probabilistic.

Even when relevant evidence is retrieved, the model may:

- Misinterpret evidence
- Omit an important relationship
- Make an inference that is stronger than the evidence supports
- Produce an incomplete explanation

The system therefore treats evidence grounding and abstention as important evaluation dimensions rather than assuming that correct retrieval guarantees a correct answer.

### Repository Changes

The semantic index contains embeddings generated from the repository state at index-building time.

When repository code changes, the semantic index may need to be rebuilt so that its documents and embeddings reflect the current repository.

### Performance

The current MVP uses a local language model for reasoning.

On the development CPU-only environment, LLM inference is the dominant source of query latency. The current implementation prioritizes architectural clarity and reproducibility over optimizing local inference performance.

## Future Work

The current MVP establishes the core repository-understanding pipeline. Future development can extend the system in several directions.

### Incremental Indexing

Rebuild only the semantic documents affected by repository changes instead of rebuilding the complete semantic index.

### Improved Code Understanding

Extend structural analysis to handle more complex Python constructs, including:

- Better alias and import resolution
- More complete method and attribute resolution
- Additional relationship types
- More complex factory and dynamic patterns

### Larger-Scale Retrieval

Evaluate the retrieval architecture on larger repositories and determine when a dedicated vector database or approximate nearest-neighbor infrastructure becomes useful.

### Stronger Evidence Selection

Improve evidence ranking and selection so that the reasoning model receives the most relevant supporting information while reducing unnecessary context.

### Broader Evaluation

Build a larger benchmark containing repository-level questions across different repositories and task types.

Evaluation can then compare:

1. LLM reasoning with repository context
2. Semantic retrieval with LLM reasoning
3. Structural analysis combined with semantic retrieval and LLM reasoning

This would allow the project's central hypothesis to be evaluated more systematically.

### Additional Repository Signals

Future versions could incorporate additional evidence sources such as:

- Documentation
- Configuration files
- More detailed test coverage relationships
- Version-control history
- Runtime traces

These signals could complement static and semantic analysis when static evidence alone is insufficient.

### Developer Interfaces

The current MVP exposes the system through a command-line interface.

Future versions could provide additional interfaces such as a web application or IDE integration while keeping the underlying analysis and evidence pipeline independent of the presentation layer.

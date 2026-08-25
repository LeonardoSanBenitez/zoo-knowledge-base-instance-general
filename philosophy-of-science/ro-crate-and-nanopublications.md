<!--kb
id: ro-crate-and-nanopublications
labels: metadata-standards, research-objects, linked-data, provenance, machine-readable-scholarship
triggers: how do I make a research artifact machine-describable; what is an RO-Crate; ro-crate-metadata.json; what is a nanopublication; assertion provenance publication-info graphs; is there a published standard for packaging code and data together; how do I describe workflow provenance; RO-Crate vs nanopublications; FAIR digital objects; can a review or a decision be published as structured data; which metadata standard should I use for a replication package
verified: 2026-08-25
-->

# RO-Crate and nanopublications

RO-Crate and nanopublications make different parts of scholarly communication machine-readable.
RO-Crate describes a **research object as an aggregation**: files, datasets, software, people,
instruments, licences, provenance, and their relations. A nanopublication describes a **small assertion
with its provenance and publication metadata**. They are complementary rather than competing formats.

## RO-Crate

An RO-Crate is a directory or archive containing research artifacts and a JSON-LD metadata document,
normally `ro-crate-metadata.json`. Its vocabulary is based primarily on Schema.org, with persistent
identifiers used where available. The metadata graph distinguishes the root research object from the data
entities it aggregates and the contextual entities—people, organizations, licences, places, instruments,
and other objects—needed to interpret them.

The design deliberately uses “just enough” Linked Data. A crate can remain a normal collection of files
that is inspectable without an RDF database, while JSON-LD gives it a graph interpretation for automated
processing. Domain communities can define profiles that constrain required entities and properties.

RO-Crate's natural strengths are:

- packaging heterogeneous artifacts and their metadata together;
- assigning identifiers and recording relations among files, software, agents, and outputs;
- describing provenance at research-object granularity;
- supporting profiles for particular domains or workflows;
- remaining transportable as files rather than depending on one hosted registry.

Its semantics are intentionally broad. RO-Crate does not by itself define a formal language for the
truth conditions, logical dependencies, or proof status of scientific claims. Those require a domain
profile or a separate claim model.

### Workflow provenance

Workflow Run RO-Crate extends the base model to describe computational executions, including workflow
plans, runs, inputs, outputs, code, and execution provenance at several levels of granularity. Its model
aligns with W3C PROV and was reported in 2024 as implemented by six heterogeneous workflow systems. This
illustrates the profile mechanism: interoperability comes not merely from choosing JSON-LD, but from a
community agreeing on which entities and relations have stable meanings.

## Nanopublications

A nanopublication is a small RDF publication conventionally divided into named graphs:

1. the **assertion** graph states the claim;
2. the **provenance** graph records how that assertion was derived or sourced;
3. the **publication-info** graph records authorship, creation, attribution, and publication metadata;
4. a head graph links these components.

Trusty URIs can make the artifact content-addressed: the identifier encodes a cryptographic digest of a
canonicalized representation. This supports verification that a retrieved nanopublication is the exact
immutable object identified by its URI. Nanopublications can therefore be independently hosted and
replicated while retaining verifiable identity.

Their natural strengths are:

- claim-level citation and attribution;
- explicit separation of assertion from provenance;
- immutable, globally identifiable scholarly units;
- decentralized publication and replication;
- graph queries across many small claims.

The main modeling burden is deciding what precisely belongs in the assertion graph. A textual paper
claim, a corrected claim, an interpretation under added hypotheses, and a formally verified theorem are
not interchangeable. Encoding them as one assertion would make the record machine-readable but
semantically misleading. Nanopublication quality therefore depends on disciplined vocabularies and claim
identity, not merely on RDF syntax.

## Structural comparison

| Dimension | RO-Crate | Nanopublication |
|---|---|---|
| Primary unit | a research object and its aggregated entities | one small assertion |
| Core representation | Schema.org-oriented JSON-LD graph plus files | RDF named graphs |
| Provenance emphasis | artifact, workflow, and research-object provenance | provenance of a particular assertion |
| Mutability | crates may be versioned and repackaged | normally immutable when identified by a Trusty URI |
| Human inspection | ordinary files plus readable JSON-LD | usually requires RDF-aware presentation or tooling |
| Main interoperability mechanism | shared profiles and entity vocabularies | shared assertion vocabularies, provenance relations, and persistent URIs |
| What it does not supply by itself | formal claim or proof semantics | packaging of a complete heterogeneous research object |

A research object can use both layers: an RO-Crate can aggregate data, code, documents, and
nanopublications, while the nanopublications expose selected claims and their provenance. Conversely, a
nanopublication can cite an RO-Crate or one of its entities as evidence. The important design question is
therefore not which format “wins,” but which scholarly unit needs an interoperable identity.

## Published literature and recent developments

- Soiland-Reyes et al., “Packaging research artefacts with RO-Crate,” *Data Science* 5(2), 2022,
  introduced RO-Crate as a lightweight, community-driven Schema.org/JSON-LD packaging approach and
  documented adoption in bioinformatics, digital humanities, and regulatory science.
  <https://doi.org/10.3233/DS-210053>
- Leo et al., “Recording provenance of workflow runs with RO-Crate,” *PLOS ONE* 19(9), 2024,
  specified Workflow Run RO-Crate, its alignment with W3C PROV, and implementations across six workflow
  systems. <https://doi.org/10.1371/journal.pone.0309210>
- Schlenzig et al., “RO-Crate for Testbeds: Automated Packaging of Experimental Results,” IFIP
  Networking 2024, applied RO-Crate to packaging network-testbed experiments.
  <https://doi.org/10.23919/IFIPNetworking62109.2024.10619057>
- Soiland-Reyes et al., “Practical webby FDOs With RO-Crate and FAIR Signposting,” 2025, examined
  RO-Crate together with FAIR Signposting as a Web-compatible implementation route for FAIR Digital
  Objects. <https://doi.org/10.52825/ocp.v5i.1273>
- Groth, Gibson, and Velterop, “The anatomy of a nanopublication,” *Information Services & Use* 30,
  2010, introduced the assertion/provenance/publication-information anatomy.
  <https://doi.org/10.3233/ISU-2010-0613>
- Kuhn et al., “Nanopublications: A Growing Resource of Provenance-Centric Scientific Linked Data,”
  IEEE eScience 2018, described the expanding decentralized nanopublication corpus and infrastructure.
  <https://doi.org/10.1109/eScience.2018.00024>
- Bucur et al., “Nanopublication-based semantic publishing and reviewing: a field study with
  formalization papers,” *PeerJ Computer Science* 9, 2023, represented submissions, reviews, responses,
  and decisions as nanopublications. The study involved 15 submissions from 18 authors and found the
  workflow technically and practically feasible, while noting the technical character of existing user
  interfaces. <https://doi.org/10.7717/peerj-cs.1159>

## Primary specifications

- RO-Crate specification: <https://www.researchobject.org/ro-crate/specification.html>
- RO-Crate 1.2 conceptual introduction: <https://www.researchobject.org/ro-crate/specification/1.2/introduction.html>
- Nanopublication Guidelines: <https://nanopub.net/guidelines/working_draft/>


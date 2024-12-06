"""Main extension code that removes non-referenced glossary terms."""
from typing import cast

from docutils import nodes
from sphinx import addnodes
from sphinx.addnodes import pending_xref
from sphinx.transforms import SphinxTransform

from . import __version__

REF_ATTR = "glossary_referenced_terms"


def purge_referenced_terms(app, env, docname):
    """Clear out any cached terms so the glossary updates on re-runs."""
    if not hasattr(env, REF_ATTR):
        return
    setattr(env, REF_ATTR, set())


def find_referenced_terms(app, doctree):
    """Gather all in-line terms while processing input.

    This is how we make a list of all terms that will show up in the glossary.
    """
    env = app.builder.env
    if not hasattr(env, REF_ATTR):
        env.glossary_referenced_terms = set()

    for node in doctree.findall(pending_xref):
        if not hasattr(node.children[0], "attributes"):
            continue
        if "std-term" in node.children[0].attributes.get("classes", []):
            term = node.attributes["reftarget"].lower()
            env.glossary_referenced_terms.add(term)


def merge_referenced(app, env, docnames, other):
    """
    Communicate gathered terms across all processes.

    Only relevant if running in parallel with -N auto, etc.
    """
    if not hasattr(env, REF_ATTR):
        env.glossary_referenced_terms = set()

    if hasattr(other, REF_ATTR):
        env.glossary_referenced_terms.add(other.glossary_referenced_terms)


class GlossaryReferencedFilterer(SphinxTransform):
    """
    Filter glossaries showing only terms that are referenced in the text.

    This is a post-processing transform that occurs after all xrefs are
    resolved.
    """

    default_priority = 500

    def apply(self, **kwargs) -> None:
        """Apply the filter."""
        referenced = self.env.glossary_referenced_terms

        for glossary in self.document.findall(addnodes.glossary):
            definition_list = cast(nodes.definition_list, glossary[0])
            filtered_definition_list = cast(nodes.definition_list, [])

            for definition in definition_list:
                term = definition[0].astext().lower()
                if term in referenced:
                    filtered_definition_list.append(definition)
            definition_list[:] = filtered_definition_list


def setup(app):
    """Set up extension."""
    app.connect("doctree-read", find_referenced_terms)
    app.connect("env-merge-info", merge_referenced)
    app.add_post_transform(GlossaryReferencedFilterer)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

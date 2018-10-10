import markdown
import requests
from bs4 import BeautifulSoup
from jinja2 import Template

import re


class SectionHeadersDoNotExist(Exception):
    pass


def parse_section(doc, section_start, section_end):
    """
    Parse section of Markdown text from `section_start` to `section_end`.
    - If `section_start` is `None`, then the document is parsed form the
      beginning to the `section_end` header.
    - If `section_end` is `None`, then the entire document is parsed until
        `section_end` is found.

    Note:
    ------
    If the `SectionHeadersDoNotExist` Exception is raised, check to make sure
    the correct tag is compiled into the regex expression used in the
    `soup.find_all` call.


    returns:
    --------
    HTML that was rendered from Markdown
    """
    doc = doc.replace("#.#.#", "\#.\#.\#")
    html = markdown.markdown(doc)
    if section_start is None:
        get_next = True
    else:
        get_next = False
    soup = BeautifulSoup(html, "html.parser")
    data = []
    for node in soup.find_all(re.compile("p|h[1-6]|ul|li")):
        if node.text == section_start:
            get_next = True
            continue
        if get_next:
            if section_end is None:
                data.append(str(node))
            elif section_end not in node.text:
                data.append(str(node))
            else:
                break
    if len(data) == 0:
        raise SectionHeadersDoNotExist(
            f"{section_start} and/or {section_end} was not found."
        )
    return " ".join(data)


def render_template(template_path, **render_kwargs):
    """
    Helper method to render the template file and context.

    returns:
    --------
    rendered html
    """
    with open(template_path, "r") as f:
        template_str = f.read()
    template = Template(template_str)
    return template.render(**render_kwargs)


def data_from_url(url, start_header, end_header):
    resp = requests.get(url)
    text = resp.text
    return parse_section(text, start_header, end_header)


namemap = {
    "key_features": "Key Features",
    "project_overview": "Project Overview",
    "citation": "Citation",
    "license": "License",
    "user_documentation": "User Documentation",
    "user_changelog_recent": "User Changelog Recent",
    "user_changelog": "User Changelog",
    "dev_changelog": "Developer Changelog",
    "disclaimer": "Disclaimer",
    "user_case_studies": "User Case Studies",
    "project_roadmap": "Project Roadmap",
    "contributor_overview": "Contributor Overview",
    "contributor_guide": "Contributor Guide",
    "governance_overview": "Governance Overview",
    "public_funding": "Public Funding",
    "link_to_webapp": "Link to webapp",
    "public_issue_tracker": "Public Issue Tracker",
    "public_qanda": "Public Q & A",
}

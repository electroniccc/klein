
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import json

from klein.plating import Plating
from twisted.web.template import tags, slot

from klein.test.test_resource import requestMock, _render
from klein.test.util import TestCase
from klein import Klein

plating = Plating(
    defaults=dict(
        title="JUST A TITLE",
        content="NEVER MIND THE CONTENT",
    ),
    tags=tags.html(
        tags.head(tags.title(slot("title"))),
        tags.body(
            tags.h1(slot("title")),
            tags.div(slot("content"),
                     Class="content")
        )
    ),
)


class PlatingTests(TestCase):
    """
    Tests for L{Plating}.
    """

    def setUp(self):
        """
        Create an app and a resource wrapping that app for this test.
        """
        self.app = Klein()
        self.kr = self.app.resource()

    def test_template(self):
        """
        Rendering a L{Plating.routed} decorated route results in templated
        HTML.
        """
        @plating.routed(self.app.route("/"),
                        tags.span(slot("ok")))
        def plateMe(request):
            return {"ok": "test-data-present"}

        request = requestMock(b"/")
        d = _render(self.kr, request)
        self.successResultOf(d)
        written = request.getWrittenData()
        self.assertIn(b'<span>test-data-present</span>', written)
        self.assertIn(b'<title>JUST A TITLE</title>', written)

    def test_template_json(self):
        """
        Rendering a L{Plating.routed} decorated route with a query parameter
        asking for JSON will yield JSON instead.
        """
        @plating.routed(self.app.route("/"),
                        tags.span(slot("ok")))
        def plateMe(request):
            return {"ok": "an-plating-test"}

        request = requestMock(b"/?json=true")

        d = _render(self.kr, request)
        self.successResultOf(d)

        written = request.getWrittenData()
        print("what", repr(written))
        self.assertEquals({"ok": "an-plating-test", "title": "JUST A TITLE"},
                          json.loads(written))


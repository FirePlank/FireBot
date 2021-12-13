import json
import httpx as requests
from . import utils

class Perspective(object):

    base_url = "https://commentanalyzer.googleapis.com/v1alpha1"

    def __init__(self, key):
        self.key = key

    def score(self, text, tests=None, do_not_store=False, token=None, text_type=None):
        # data validation
        # make sure it's a valid test
        # TODO: see if an endpoint that has valid types exists
        if isinstance(tests, str):
            tests = [tests]
        if not isinstance(tests, (list, dict)) or tests is None:
            raise ValueError("Invalid list/dictionary provided for tests")
        if isinstance(tests, list):
            new_data = {}
            for test in tests:
                new_data[test] = {}
            tests = new_data
        if text_type:
            if text_type.lower() == "html":
                text = utils.remove_html(text)
            elif text_type.lower() == "md":
                text = utils.remove_html(text, md=True)
            else:
                raise ValueError("{0} is not a valid text_type. Valid options are 'html' or 'md'".format(str(text_type)))

        # packaging data
        url = Perspective.base_url + "/comments:analyze"
        querystring = {"key": self.key}
        payload_data = {"comment": {"text": text}, "requestedAttributes": {}}
        for test in tests.keys():
            payload_data["requestedAttributes"][test] = tests[test]
        payload_data["languages"] = ['en']
        if do_not_store:
            payload_data["doNotStore"] = do_not_store
        payload = json.dumps(payload_data)
        headers = {'content-type': "application/json"}
        response = requests.post(url, data=payload, headers=headers, params=querystring, timeout=2)
        data = response.json()
        if "error" in data.keys():
            raise PerspectiveAPIException(data["error"]["message"])
        c = Comment(text, [], token)
        base = data["attributeScores"]
        for test in tests.keys():
            score = base[test]["summaryScore"]["value"]
            score_type = base[test]["summaryScore"]["type"]
            a = Attribute(test, [], score, score_type)
            for span in base[test]["spanScores"]:
                beginning = span["begin"]
                end = span["end"]
                score = span["score"]["value"]
                score_type = span["score"]["type"]
                s = Span(beginning, end, score, score_type, c)
                a.spans.append(s)
            c.attributes.append(a)
        return c


class Comment(object):
    def __init__(self, text, attributes, token):
        self.text = text
        self.attributes = attributes
        self.token = token

    def __getitem__(self, key):
        for attr in self.attributes:
            if attr.name.lower() == key.lower():
                return attr
        raise ValueError("value {0} not found".format(key))

    def __str__(self):
        return self.text

    def __repr__(self):
        count = 0
        num = 0
        for attr in self.attributes:
            count += attr.score
            num += 1
        return "<({0}) {1}>".format(str(count/num), self.text)

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.text)


class Attribute(object):
    def __init__(self, name, spans, score, score_type):
        self.name = name
        self.spans = spans
        self.score = score
        self.score_type = score_type

    def __getitem__(self, index):
        return self.spans[index]

    def __iter__(self):
        return iter(self.spans)


class Span(object):
    def __init__(self, begin, end, score, score_type, comment):
        self.begin = begin
        self.end = end
        self.score = score
        self.score_type = score_type
        self.comment = comment

    def __str__(self):
        return self.comment.text[self.begin:self.end]

    def __repr__(self):
        return "<({0}) {1}>".format(self.score, self.comment.text[self.begin:self.end])


class PerspectiveAPIException(Exception):
    pass

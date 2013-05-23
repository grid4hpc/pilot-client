# -*- encoding: utf-8 -*-

from ... import formats
from .. import tests

job_wrong = """
{ "version": 2,
  "tasks": [ { "id": "a",
               "definition": {
                   "version": 2,
                   "executable": "/bin/true",
                   "requirements": { "hostname": ["tb01.ngrid.ru"],
                                     "foo": "bar" }
               }
              } ]
}
"""

def test_pass():
    formats.job_loads(tests.minimal_job)

def test_fail():
    try:
        formats.job_loads(job_wrong)
    except ValueError, e:
        assert str(e) == "Additional property 'foo' not defined by 'properties' is not allowed in field '_data'"
    else:
        raise ValueError("expected failure for job_wrong")

import unittest
from engine.classifier import classify_relation
from engine.validator import validate_topothink_hypergraph

class TestEngine(unittest.TestCase):
    def test_classification_joints(self):
        # 1. Containment
        self.assertEqual(classify_relation("contains"), "containment")
        self.assertEqual(classify_relation("subnet_of"), "containment")

        # 2. State Change
        self.assertEqual(classify_relation("next_paragraph"), "state_change")
        self.assertEqual(classify_relation("transitions_to"), "state_change")

        # 3. Interactivity
        self.assertEqual(classify_relation("hires"), "interactivity")
        self.assertEqual(classify_relation("marries"), "interactivity")
        self.assertEqual(classify_relation("imports", is_runtime=True), "interactivity")

        # 4. Reference
        self.assertEqual(classify_relation("cites"), "reference")
        self.assertEqual(classify_relation("imports", is_runtime=False), "reference")

    def test_schema_validator(self):
        valid_doc = {
            "nodes": [{"id": "a"}, {"id": "b"}],
            "edges": [{"id": "e1", "directed": True}],
            "incidences": [
                {"edge": "e1", "node": "a", "role": "source"},
                {"edge": "e1", "node": "b", "role": "target"}
            ]
        }
        ok, errs = validate_topothink_hypergraph(valid_doc)
        self.assertTrue(ok)
        self.assertEqual(errs, [])

        # Missing role on directed edge
        invalid_doc = {
            "nodes": [{"id": "a"}, {"id": "b"}],
            "edges": [{"id": "e1", "directed": True}],
            "incidences": [
                {"edge": "e1", "node": "a"},
                {"edge": "e1", "node": "b"}
            ]
        }
        ok, errs = validate_topothink_hypergraph(invalid_doc)
        self.assertFalse(ok)
        self.assertTrue(len(errs) > 0)

if __name__ == "__main__":
    unittest.main()

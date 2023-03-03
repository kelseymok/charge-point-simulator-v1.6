from helpers import flatten_list_of_lists, pulse


class TestHelpers:

    def test_flatten_list_of_lists(self):
        l = [
                ["a","b","c"],
                ["d","e", "f"]
        ]
        result = flatten_list_of_lists(l)
        assert result == ["a", "b", "c", "d", "e", "f"]

    def test_pulse(self):
        starting_time = "2023-01-01T09:00:00+00:00"
        ending_time = "2023-01-01T09:10:00+00:00"
        f = lambda x, **kwargs: x + 1
        result = pulse(
            f, starting_time, ending_time, x=2
        )
        assert result == [
            (3, "2023-01-01T09:00:00+00:00"),
            (3, "2023-01-01T09:05:00+00:00")
        ]
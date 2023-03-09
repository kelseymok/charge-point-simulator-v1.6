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
        f_request = lambda x, **kwargs: x + 5
        f_response = lambda x, **kwargs: x + 10
        requests, responses = pulse(
            f_request=f_request,
            f_response=f_response,
            starting_time=starting_time,
            ending_time=ending_time, x=2
        )
        assert requests == [(7, '2023-01-01T09:00:00+00:00'), (7, '2023-01-01T09:05:00+00:00')]
        assert responses == [(12, '2023-01-01T09:00:01+00:00'), (12, '2023-01-01T09:05:01+00:00')]
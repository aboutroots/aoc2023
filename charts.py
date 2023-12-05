import enum
from typing import List, Union, Optional

import numpy as np
import pytest
from termcolor import colored


class Direction(enum.Enum):
    T = "TOP"
    R = "RIGHT"
    B = "BOTTOM"
    L = "LEFT"


class Point:
    def __init__(self, x: int, y: int):
        if x < 0 or y < 0:
            raise AttributeError(f"Coordinates cannot be negative, x:{x} y:{y}")
        self.x = x
        self.y = y

    def __repr__(self):
        return f"P<{self.x},{self.y}>"

    def __eq__(self, other: "Point"):
        return self.x == other.x and self.y == other.y


class Block:
    def __init__(self, anchor: Point, pixels: List[List[Optional[str]]]):
        self.anchor = anchor
        self.points = self._get_points_for_pixels(pixels)
        self._initial_pixels = pixels

    def _get_points_for_pixels(self, pixels) -> List[Point]:
        points = []
        for row_idx, row in enumerate(pixels):
            for col_idx, value in enumerate(row):
                if value is not None:
                    points.append(
                        Point(
                            x=self.anchor.x + col_idx, y=self.anchor.y + row_idx
                        )
                    )
        return points

    def update_points_and_anchor(self, points: List[Point]):
        self.points = points
        self.anchor = Point(
            x=min(p.x for p in points), y=min(p.y for p in points)
        )


class Chart:
    def __init__(
        self,
        width: int,
        height: int,
        default_fill: str = ".",
        value_fill: str = "#",
    ):
        self._empty_fill = default_fill
        self._value_fill = value_fill
        self._chart = np.full((height, width), ".")

    @property
    def dimensions(self):
        """(width, height)"""
        return tuple(reversed(self._chart.shape))

    @property
    def max_filled_y(self):
        """Return max row with at least one filled value"""
        return max(np.where(self._chart == self._value_fill)[0])

    @property
    def max_filled_y_per_column(self):
        ch = self._chart.transpose()
        result = []
        for column in ch:
            values = list(np.where(column == self._value_fill)[0])
            result.append(max(values) if values else 0)
        return result

    def __eq__(self, other: "Chart"):
        for row_idx, row in enumerate(self._chart):
            if not "".join(row) == "".join(other._chart[row_idx]):
                return False
        return True

    def __iter__(self):
        for row in self._chart:
            yield row

    def __reversed__(self):
        for row in reversed(self._chart):
            yield row

    def __getitem__(self, item):
        return self._chart[item]

    def print(
        self,
        x_from=None,
        x_to=None,
        y_from=None,
        y_to=None,
        with_points: Optional[List[Point]] = None,
        flip_y_axis: bool = False,
        label_y_axis: bool = False,
    ):
        def _colorize_pixel(val, y, x):
            if val != self._empty_fill:
                return colored(val, color="red", attrs=["bold"])
            if with_points:
                if Point(x, y) in with_points:
                    return colored("@", color="green", attrs=["bold"])
            return val

        x_from = x_from or 0
        y_from = y_from or 0
        x_to = x_to or self.dimensions[0] + 1
        y_to = y_to or self.dimensions[1] + 1

        print()
        rows_to_print = []
        for row_idx, row in enumerate(self._chart[y_from:y_to], start=y_from):
            row_to_print = []
            for col_idx, col in enumerate(row[x_from:x_to], start=x_from):
                row_to_print.append(_colorize_pixel(col, row_idx, col_idx))
            rows_to_print.append("".join(row_to_print))

        len_of_rows = len(rows_to_print)
        if flip_y_axis:
            rows_to_print = reversed(rows_to_print)
        for idx, joined_row in enumerate(rows_to_print):
            print_idx = idx if not flip_y_axis else len_of_rows - 1 - idx
            row_to_print = (
                joined_row
                if not label_y_axis
                else f"{print_idx:02d}: {joined_row}"
            )
            print(row_to_print)

    def set(self, p: Point, fill: Optional[str] = None) -> bool:
        """
        :return: True if was able to set the value on map, False otherwise
        """
        fill = fill if fill is not None else self._value_fill
        try:
            self._chart[p.y, p.x] = fill
            return True
        except IndexError:
            return False

    def set_column(self, x: int, fill: Optional[str] = None):
        self._chart[:, x] = fill if fill is not None else self._value_fill

    def set_row(self, y: int, fill: Optional[str] = None):
        self._chart[y, :] = fill if fill is not None else self._value_fill

    def get(self, p: Point) -> Optional[str]:
        """
        :return: Value from map on given point, None on index error
        """
        try:
            return self._chart[p.y, p.x]
        except IndexError:
            return None

    def is_empty(self, p: Point) -> bool:
        value = self.get(p)
        return value == self._empty_fill

    def is_full_row(self, y: int) -> bool:
        row = self._chart[y]
        return all(v == self._value_fill for v in row)

    def get_neighbours_points(
        self, p: Point, with_diagonals=False
    ) -> List[Optional[Point]]:
        """
        Returns neighbours clockwise starting from top, None if not exists
        """
        directions_yx = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        if with_diagonals:
            directions_yx = [
                (-1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
                (1, 0),
                (1, -1),
                (0, -1),
                (-1, -1),
            ]
        neighbours = []
        for t in directions_yx:
            try:
                next_point = Point(y=p.y + t[0], x=p.x + t[1])
                neighbours.append(next_point)
            except AttributeError:
                neighbours.append(None)
        return neighbours

    def get_neighbours(
        self, p: Point, with_diagonals=False
    ) -> List[Optional[str]]:
        """
        Returns neighbours clockwise starting from top, None if not exists
        """
        ns = []
        for point in self.get_neighbours_points(p, with_diagonals):
            if point:
                ns.append(self.get(point))
            else:
                ns.append(None)
        return ns

    def get_neighbor(self, p: Point, direction: Direction) -> Optional[Point]:
        indexes = [Direction.T, Direction.R, Direction.B, Direction.L]
        neighbours = self.get_neighbours_points(p)
        return neighbours[indexes.index(direction)]

    def move_all_up(self, n_rows: int) -> None:
        """Move all rows to the top (discard first n rows). Fill the remaining
        space with default empty fill.
        """
        if n_rows <= 0:
            raise AttributeError("n_rows parameter must be positive")
        temp = self._chart[n_rows:, :]
        self._chart[:-n_rows, :] = temp
        self._chart[-n_rows:, :] = self._empty_fill


class TestChart:
    @pytest.fixture
    def chart(self):
        """
        Chart with the following layout
        ...
        ...
        #@.
        .$.
        ...
        """
        chart = Chart(3, 5)
        chart.set(Point(x=0, y=2))
        chart.set(Point(x=1, y=2), fill="@")
        chart.set(Point(x=1, y=3), fill="$")
        return chart

    def test_print_does_not_throw_errors(self, chart):
        chart.print()
        chart.print(x_from=1, x_to=2, y_from=1, y_to=4)

    def test_get_neighbours_returns_correct_values(self, chart):
        ns = chart.get_neighbours(Point(0, 2))
        assert ns == [".", "@", ".", None]
        ns = chart.get_neighbours(Point(1, 2))
        assert ns == [".", ".", "$", "#"]

    def test_get_neighbours_returns_correct_values_with_diagonals(self, chart):
        ns = chart.get_neighbours(Point(0, 2), with_diagonals=True)
        assert ns == [".", ".", "@", "$", ".", None, None, None]
        ns = chart.get_neighbours(Point(1, 2), with_diagonals=True)
        assert ns == [".", ".", ".", ".", "$", ".", "#", "."]

    def test_get_dimensions(self, chart):
        assert chart.dimensions == (3, 5)

    def test_equals(self, chart):
        chart_2 = Chart(3, 5)
        assert chart != chart_2
        chart_2.set(Point(x=0, y=2))
        chart_2.set(Point(x=1, y=2), fill="@")
        chart_2.set(Point(x=1, y=3), fill="$")
        assert chart == chart_2

    def test_can_set_column(self, chart):
        x = 1
        chart.set_column(x, "X")
        for row in chart:
            for index, value in enumerate(row):
                assert value == "X" if index == x else value != "X"

    def test_can_set_row(self, chart):
        y = 1
        chart.set_row(y, "Y")
        for index, row in enumerate(chart):
            assert (
                all(value == "Y" for value in row)
                if index == y
                else all(value != "Y" for value in row)
            )

    def test_max_y(self, chart):
        assert chart.max_filled_y == 2
        chart.set(Point(x=2, y=4), "#")
        assert chart.max_filled_y == 4

    def test_move_all_up(self, chart):
        chart.move_all_up(1)
        chart.print()

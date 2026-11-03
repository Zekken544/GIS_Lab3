"""Generate four points and four rectangles and report all containment checks."""
from dataclasses import dataclass
from pathlib import Path
from random import Random


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Rectangle:
    xmin: int
    ymin: int
    xmax: int
    ymax: int

    def contains(self, point):
        return self.xmin <= point.x <= self.xmax and self.ymin <= point.y <= self.ymax


def main():
    random = Random(42)
    points = [Point(random.randrange(11), random.randrange(11)) for _ in range(4)]
    rectangles = []
    for _ in range(4):
        xmin, xmax = sorted(random.sample(range(11), 2))
        ymin, ymax = sorted(random.sample(range(11), 2))
        rectangles.append(Rectangle(xmin, ymin, xmax, ymax))
    lines = [f"R{i}: {rect}" for i, rect in enumerate(rectangles, 1)]
    for i, point in enumerate(points, 1):
        for j, rectangle in enumerate(rectangles, 1):
            status = "inside" if rectangle.contains(point) else "outside"
            lines.append(f"P{i} ({point.x}, {point.y}) / R{j}: {status}")
    report = "\n".join(lines) + "\n"
    Path("intersections.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    main()

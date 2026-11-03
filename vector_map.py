"""Read the section 5.6.1 polyline format and draw it with Tkinter."""
import argparse
from math import dist, isfinite
from pathlib import Path
import re


def read_polylines(path):
    header, separator, body = path.read_text(encoding="utf-8-sig").partition(";")
    if not separator or header.strip().lower() != "polyline":
        raise ValueError("Expected a Polyline; header")
    polylines = {}
    points = None
    for token in body.split(";"):
        if not token.strip():
            continue
        match = re.fullmatch(r"\s*(\d+)\s*:\s*(.*)", token, flags=re.DOTALL)
        if match:
            identifier, token = match.groups()
            if identifier in polylines:
                raise ValueError(f"Duplicate polyline {identifier}")
            points = polylines[identifier] = []
        if points is None:
            raise ValueError("A polyline must start with its identifier")
        x, y = map(float, token.split(","))
        if not (isfinite(x) and isfinite(y)):
            raise ValueError("Coordinates must be finite")
        points.append((x, y))
    if not polylines or any(len(vertices) < 2 for vertices in polylines.values()):
        raise ValueError("Each polyline needs at least two vertices")
    return polylines, len(next(iter(polylines.values())))


def screen_transform(points, width, height, padding=30):
    xs, ys = zip(*points)
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    scales = [pixels / span for pixels, span in
              [(width - 2 * padding, xmax - xmin), (height - 2 * padding, ymax - ymin)]
              if span]
    scale = min(scales, default=1)
    return lambda x, y: (width / 2 + (x - (xmin + xmax) / 2) * scale,
                         height / 2 - (y - (ymin + ymax) / 2) * scale)


def show_map(polylines):
    import tkinter as tk

    width, height = 800, 520
    root = tk.Tk()
    root.title("GIS Lab 3 — Vector data")
    canvas = tk.Canvas(root, width=width, height=height, background="white")
    canvas.pack()
    transform = screen_transform([p for line in polylines.values() for p in line], width, height)
    for identifier, line in polylines.items():
        coords = [value for point in line for value in transform(*point)]
        if line[0] == line[-1]:
            canvas.create_polygon(*coords, fill="#d7eee5", outline="#157a6e", width=2)
        else:
            canvas.create_line(*coords, fill="#2855a0", width=2)
        x, y = transform(*line[0])
        canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#e34a33", outline="")
        canvas.create_text(x + 8, y - 10, text=identifier, anchor="w")
    root.mainloop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path, default=Path(__file__).with_name("polylines.txt"))
    parser.add_argument("--no-gui", action="store_true")
    args = parser.parse_args()
    try:
        polylines, first_count = read_polylines(args.input)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    print(f"First polyline: {first_count} vertices")
    for identifier, line in polylines.items():
        length = sum(dist(a, b) for a, b in zip(line, line[1:]))
        print(f"{identifier}: {len(line)} vertices, length={length:.3f}")
    if not args.no_gui:
        show_map(polylines)


if __name__ == "__main__":
    main()

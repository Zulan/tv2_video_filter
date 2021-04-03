import os
import subprocess
import time

import click
import cv2 as cv

resolution = 2560, 1440
check_pos = 54, 2529
active_range = 60, 74


@click.command()
@click.argument("input-file", type=click.Path(exists=True))
@click.option("--output-file", type=click.Path(exists=False), default=None)
@click.option("--open/--no-open", default=False)
@click.option("--open-cmd", default="xdg-open")
@click.option("--fourcc", default="mp4v")
def main(input_file, output_file, open, open_cmd, fourcc):
    if output_file is None:
        base_name, ext = os.path.splitext(input_file)
        output_file = base_name + "-active" + ext
    cap = cv.VideoCapture(input_file)
    fps = cap.get(cv.CAP_PROP_FPS)
    total_frames = cap.get(cv.CAP_PROP_FRAME_COUNT)
    click.echo(
        f"reading {input_file}: {fps} fps, frames {total_frames}, time {total_frames / fps} s"
    )
    writer = cv.VideoWriter(
        output_file, cv.VideoWriter_fourcc(*fourcc), fps, resolution
    )
    frames = 0
    active_frames = 0

    def show_extra(_):
        try:
            return f"[active {active_frames / fps:0.1f} s of {frames / fps:0.1f} s {100 * active_frames / frames:2.1f} %]"
        except ZeroDivisionError:
            return ""

    with click.progressbar(
        length=int(total_frames),
        label="cutting video",
        show_eta=True,
        show_percent=True,
        item_show_func=show_extra,
    ) as bar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            assert resolution == (frame.shape[1], frame.shape[0])
            frames += 1
            if active_range[0] < frame[check_pos][0] < active_range[1]:
                writer.write(frame)
                active_frames += 1
            bar.update(1)

    writer.release()
    click.echo(f"wrote {output_file}")

    if open:
        time.sleep(0.3)
        cmd = f'{open_cmd} "{output_file}"'
        click.echo(f"calling: {cmd}")
        subprocess.run(cmd, shell=True)
        subprocess.run


if __name__ == "__main__":
    main()

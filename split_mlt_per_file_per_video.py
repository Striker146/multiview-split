from __future__ import annotations
import argparse
import xml.etree.ElementTree as ET
import os
from dataclasses import dataclass
import subprocess
from datetime import timedelta

parser = argparse.ArgumentParser()
parser.add_argument('--mlt_path')
args = parser.parse_args()





def to_timecode(timecode_str :str):
    split = timecode_str.split(':')
    hours = int(split[0])
    minutes = int(split[1])
    seconds = float(split[2])
    time_delta = timedelta(hours=hours, minutes=minutes,seconds=seconds)
    return time_delta
    print(time_delta)

def timedelta_to_timecode(td: timedelta) -> str:
    total_seconds = td.total_seconds()
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}"

@dataclass
class VideoPath:
    output_name: str
    video_path: str
    start:str
    end:str

    def __str__(self):
        return f"{self.output_name}, {self.video_path}"


@dataclass
class Marker:        
    name: str
    start: str
    end: str


if __name__ == '__main__':
    tree = ET.parse(args.mlt_path)
    root = tree.getroot()
    videos : list[VideoPath] = []

    markers = root.find(".//properties[@name='shotcut:markers']")
    markers_list : list[Marker] = []
    profile_el = tree.getroot().find("profile")
    assert markers is not None
    for m in markers.findall('properties'):

        text = m.find("property[@name='text']").text # type: ignore
        start = m.find("property[@name='start']").text # type: ignore
        end = m.find("property[@name='end']").text # type: ignore
        assert text is not None; assert start is not None; assert end is not None
        marker = Marker(text,start,end)
        markers_list.append(marker)


    for playlist in root.findall("playlist"):
        if playlist.get("id", "").startswith("playlist"):
            entry = playlist.find('entry')
            assert entry is not None
            vid_trim_start= entry.get("in")
            vid_trim_end = entry.get('out')
            assert vid_trim_start is not None; assert vid_trim_end is not None
            chain_name = entry.get('producer')
            chain = root.find(f"chain[@id='{chain_name}']")
            assert chain is not None; assert entry is not None
            print(entry.text)

            #chain_name = chain.attrib['id']
            resource = chain.find("property[@name='resource']")
            if resource is not None:
                video_path = resource.text
                other_paths = [item.video_path for item in videos]
                print(chain_name)
                if video_path not in other_paths:
                    assert video_path is not None
                    playlist = root.findall(f".//playlist[@id='playlist']")
                    output_name = input(f"Select output name for {os.path.basename(video_path)}:")
                    videos.append(VideoPath(output_name,video_path,vid_trim_start,vid_trim_end))
    cur_path = os.getcwd()
    output_path = os.path.join(cur_path,"output")
    
    print(cur_path)
    os.makedirs(output_path,exist_ok=True)
    for marker in markers_list:
        marker_folder = os.path.join(output_path,marker.name)
        os.makedirs(marker_folder,exist_ok=True)
        sub_video_folder = os.path.join(marker_folder,'videos')
        os.makedirs(sub_video_folder,exist_ok=True)
        for vid in videos:
            frame_rate_num = profile_el.get("frame_rate_num")
            frame_rate_den = profile_el.get("frame_rate_den")
            width = profile_el.get("width")
            height = profile_el.get("height")
            progressive = profile_el.get("progressive")

            start = to_timecode(vid.start) + to_timecode(marker.start)
            end = to_timecode(vid.start) + to_timecode(marker.end)
            start_str = timedelta_to_timecode(start)
            end_str = timedelta_to_timecode(end)
            length = end - start
            print(f"Completing {marker.name}, {vid.output_name}, video length : {length} ")
            video_output_path = os.path.join(sub_video_folder, f'{vid.output_name}.mp4')
            command = ["melt.exe",
                f"{vid.video_path}",
                f"in={start_str}",
                f"out={end_str}",
                f"frame_rate_num={frame_rate_num}",
                f"frame_rate_den={frame_rate_den}",
                f"width={width}",
                f"height={height}",
                f"progressive={progressive}",
                "-consumer",
                f'avformat:{video_output_path}']
            result = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=600)
            #print(result.stderr)
            #print(result.stdout)
            

    print(videos)
    
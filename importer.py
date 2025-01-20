'''
Copyright 2025 Barcelli Pte Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import unreal
import csv
import math
import sys

def ExpandCsv(csvPath):
    data = []
    with open(csvPath, 'r', newline='', encoding='utf-8') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            data.append(row)
    return data


def SpawnAssets(data, meshFolderPath):

    success = unreal.EditorLevelLibrary.new_level(meshFolderPath + "/import.import")
    if success:
        print("this success")
        unreal.EditorLevelLibrary.save_current_level()
        unreal.EditorLevelLibrary.load_level(meshFolderPath + "/import.import")
    else:
        print("Error: Previous import level detected. Please delete it and run the script again")
        sys.exit(1)


    i = 1
    while i < len(data):
        assetPath = meshFolderPath + "/" + data[i][1].replace(".", "_") + "." + data[i][1].replace(".", "_")
        asset = unreal.EditorAssetLibrary.load_asset(assetPath)
        if not asset:
            print(f"Error: Failed to load asset at path: {assetPath}")
            sys.exit(1)
        else:
            location = unreal.Vector(
                    float(data[i][2]),
                    -float(data[i][3]),
                    float(data[i][4])
                    )
            scale = unreal.Vector(
                    float(data[i][5]),
                    float(data[i][6]),
                    float(data[i][7])
                    )
            rotation = unreal.Rotator(
                    math.degrees(float(data[i][8])),
                    -math.degrees(float(data[i][9])), 
                    -math.degrees(float(data[i][10])),
                    )

            spawnAsset = unreal.EditorLevelLibrary.spawn_actor_from_object(asset, location, rotation)

            spawnAsset.set_actor_scale3d(scale)
            #deltaRotation = unreal.Rotator(180, 0, 90)
            #spawnAsset.add_actor_world_rotation(deltaRotation, False, True)
            i += 1

def main():
    if len(sys.argv) != 2:
        print("Usage: ue_importer.py <mesh_folder_path>")
        print("Example: ue_importer.py /Game/StaticMeshes")
        sys.exit(1)


    meshFolderPath = sys.argv[1]

    contentDir = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_content_dir())
    if not unreal.Paths.directory_exists(contentDir + meshFolderPath.replace("/Game/", "")):
        print(f"Error: {meshFolderPath} doesn't exist")
        sys.exit(1)

    csvPath = contentDir + meshFolderPath.replace("/Game/", "") + "/location_data.csv"

    data = ExpandCsv(csvPath)
    SpawnAssets(data, meshFolderPath)

if __name__ == "__main__":
    main()

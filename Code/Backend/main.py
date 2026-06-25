from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse 
from pyproj import Transformer
import pickle
from rasterio.transform import Affine
import networkx as nx


app = FastAPI()


reqTrans = Transformer.from_crs('EPSG:4326','EPSG:32645', always_xy=True)
resTrans = Transformer.from_crs('EPSG:32645','EPSG:4326', always_xy=True)
print("Loading Graph")
def loadGraph(): #Loads the graph when server starts
    with open(r"D:\Resume Projs\EcoRouteAI\Dataset\costGraph.gpickle","rb") as src:
        g= pickle.load(src)
        gTrans = g.graph['transform']
        frwdTrans = Affine(*gTrans[:6])
        inverTrans= ~frwdTrans
    return g, frwdTrans, inverTrans

def transformCoords(x, y, trans): #Transfroms from EPSG4326 to EPSG32645 and vice versa
    return trans.transform(x,y)

def findMax(i): #Finds the max row/col
    return max(node[i] for node in g.nodes)+1

def coordToNode(est: float, nth: float, maxRow, maxCol):    #Converts Coordinates to Nodes
    col,row = inverTrans *(est,nth)
    row = int(round(row))
    col = int(round(col))

    row = max(0, min(row, maxRow -1))
    col = max(0, min(col, maxCol-1))

    return (row,col)


def manhattenHeur(a,b): #Manhatten over Euclidean for Grid-like Graphs
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def findPath(start,end): #performs A* and converts path to EPSg4326

    path = nx.astar_path(g, start,end, heuristic=manhattenHeur, weight = 'weight')
    jsonCoords = []
    for row,col in path:
        est,nth = frwdTrans * (col+0.5, row+0.5)

        lon,lat = transformCoords(est,nth, resTrans)
        jsonCoords.append([lon,lat])
    return jsonCoords

g, frwdTrans, inverTrans = loadGraph()

maxRow = findMax(0)
maxCol = findMax(1)

@app.get("/findRoute")
def findRoute(src: str, dst: str): #src and dst would be strings like: src=lon,lat&dst=long,lat
    try:
        srclon, srclat = map(float, src.split(","))
        dstlon, dstlat = map(float, dst.split(",")) #Extracted the Co-ordinates

        srcest, srcnth = transformCoords(srclon, srclat, reqTrans) #CRS Conversion
        dstest, dstnth = transformCoords(dstlon, dstlat, reqTrans)


        start = coordToNode(srcest, srcnth, maxRow, maxCol)
        end = coordToNode(dstest, dstnth, maxRow, maxCol)

        path = findPath(start, end)

        return JSONResponse(content={
            "type":"Feature",
            "properties":{
                "engine":"NetworkX-AStar",
                "Path Length": len(path)
            },
            "geometry":{
                "type":"LineString",
                "coordinates": path,
            },
        })
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No valid path found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Routing calculation failed: {str(e)}")


    
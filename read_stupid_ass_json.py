import json
import matplotlib.pyplot as plt
import numpy as np

from shot_params import extract_pre_post

def convert_fucked_decimal(list_in):
    list_out = []
    for i in range(0,len(list_in),2):
        decimal = list_in[i+1]
        while decimal > 1:
            decimal /= 10
        list_out.append(list_in[i]+decimal)
    return list_out

with open("flat.json", "r") as f:
    flat = json.load(f)
with open("lob.json", "r") as f:
    lob = json.load(f)
with open("topspin.json", "r") as f:
    topspin = json.load(f)

def extract_series(json_in):
    out_dict = {}
    for entry in json_in["series"]:
        out_dict[entry["name"]] = entry["y"]
    return out_dict

flat_extract = extract_series(flat)
lob_extract = extract_series(lob)
top_extract = extract_series(topspin)

flat_vy = convert_fucked_decimal(flat_extract["vy"])
flat_vh = convert_fucked_decimal(flat_extract["v§h"])
lob_vy = convert_fucked_decimal(lob_extract["vy"])
lob_vh = convert_fucked_decimal(lob_extract["v§h"])
top_vy = convert_fucked_decimal(top_extract["vy"])
top_vh = convert_fucked_decimal(top_extract["v§h"])

flat_pre_vy, flat_post_vy, flat_pre_vh, flat_post_vh = extract_pre_post(flat_vy, flat_vh)
lob_pre_vy, lob_post_vy, lob_pre_vh, lob_post_vh = extract_pre_post(lob_vy, lob_vh)
top_pre_vy, top_post_vy, top_pre_vh, top_post_vh = extract_pre_post(top_vy, top_vh)

fig, (ax1, ax2) = plt.subplots(1,2)
ax1.scatter(flat_pre_vy, flat_post_vy, label="flat")
ax1.scatter(lob_pre_vy, lob_post_vy, label="lob")
ax1.scatter(top_pre_vy, top_post_vy, label="topspin")
x = np.linspace(-25,-5,5)
y = -0.75*x+1
y2 = -1.05*x+2
ax1.plot(x,y)
ax1.plot(x,y2)
ax1.legend()


ax2.scatter(flat_pre_vh, flat_post_vh)
ax2.scatter(lob_pre_vh, lob_post_vh)
ax2.scatter(top_pre_vh, top_post_vh)
x = np.linspace(10,30,5)
y = 0.95*x
y2 = 1.1*x
ax2.plot(x,y)
ax2.plot(x,y2)

plt.savefig("plot.png")
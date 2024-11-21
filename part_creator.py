import  tkinter 
import  openpyscad as ops
import os
import subprocess
import time

def save_dxf(inf, outf):
    # Путь к OpenSCAD файлу
    scad_file = inf
    # Имена выходных файлов
    #output_stl = f"part_{width}x{length}x{thickness}.stl"
    output_dxf = f"{outf}.dxf"
    # Проверка, что файл OpenSCAD существует
    if not os.path.exists(scad_file):
        print(f"Файл {scad_file} не найден.")
        return
    dxf_command = [
        "C:\\Program Files\\OpenSCAD\\openscad.exe",  # Полный путь к OpenSCAD
        "-o", output_dxf,
        scad_file
    ]
    try:
        # Запуск команды для DXF
        subprocess.run(dxf_command, check=True)
        print(f"DXF файл {output_dxf} создан.")
    except subprocess.CalledProcessError as e:
        print("Ошибка при генерации файлов:", e)

def add_perf_elem(t,x,y):
    m1 = ops.Difference()
    ci = ops.Circle(1.5,3,100).translate([5,5,0])
    cu = ops.Square(10)
    m1.append(cu)
    m1.append(ci)
    m1 = m1.translate([x,y,0])
    t.append(m1)

def add_elem(t,x,y):
    cu = ops.Square(10)
    cu = cu.translate([x,y,0])
    t.append(cu)

def add_vg(t,x,y,o):
    elem_vg = ops.Difference()
    base = ops.Square(10)
    vg = ops.Union()
    v = ops.Square([10,3]).translate([-5,-1.5])
    g = ops.Square([2.5,5.5]).translate([-1.25,-2.75])
    vg.append(v)
    vg.append(g)
    if(o == "-"):
        pass
    elif(o == "|"):
        vg =vg.rotate([0,0,90])
    vg = vg.translate([5,5,0])
    elem_vg.append(base)
    elem_vg.append(vg)
    elem_vg = elem_vg.translate([x,y,0])
    t.append(elem_vg)
def add_alt_vg(t,x,y,o):
    vg = ops.Union()
    v = ops.Square([13,3]).translate([-6.5,-1.5])
    g = ops.Square([2.5,5.5]).translate([-1.25,-2.75])
    vg.append(v)
    vg.append(g)
    if(o == ">"):
        vg = vg.translate([x+6.5,y+5,0])
        vg = vg.color("red")
    elif(o == "<"):
        vg = vg.rotate([0,0,180])
        vg = vg.translate([x+3.5,y+5,0])
        vg = vg.color("green")
    elif(o == "v"):
        vg = vg.rotate([0,0,90])
        vg = vg.translate([x+5,y+6.5,0])
        vg = vg.color("blue")
    elif(o == "^"):
        vg = vg.rotate([0,0,-90])
        vg = vg.translate([x+5,y+3.5,0])
        vg = vg.color("Cyan")
    t.append(vg)



def gen():
    f_name = e.get()
    data =text.get("1.0", tkinter.END)
    data = data.split("\n")
    y = 0
    vg_flag = 0
    model = ops.Union()

    for module in data:
        for x in range(len(module)):
            print(module[x])
            if(module[x] == "*"):
                add_perf_elem(model,x*10,y)
            elif(module[x] == "#"):
                add_elem(model,x*10,y)
            elif(module[x] in '<>^v'):
                add_elem(model,x*10,y)
                vg_flag = 1
        y +=10
    if(vg_flag == 1):
        y = 0
        all_vg = ops.Union()

        for module in data:
            for x in range(len(module)):
                if(module[x] in '<>^v'):
                    add_alt_vg(all_vg,x*10,y,module[x])
            y +=10
        dif_m = ops.Difference()
        dif_m.append(model)
        dif_m.append(all_vg)
        dif_m.write(f"{f_name}.scad")
    else:
        model.write(f"{f_name}.scad")
    save_dxf(f"{f_name}.scad",f"{f_name}")
    L2.config(text="Готово", fg = "green")




root = tkinter.Tk()
root.geometry("400x300")
frame = tkinter.Frame(borderwidth=1)
L1 = tkinter.Label(text = "Имя файла")
L2 = tkinter.Label()
text = tkinter.Text(frame,width=36, height=12)
scroll =tkinter.Scrollbar(frame,command=text.yview,orient=tkinter.VERTICAL,)
b1 = tkinter.Button(text = "Создать DXF", command=gen)
e = tkinter.Entry()
text.config(yscrollcommand=scroll.set)

text.pack(side=tkinter.LEFT)
scroll.pack(side= tkinter.LEFT,ipady=65)

frame.pack()
L1.pack()
e.pack()
b1.pack()
L2.pack()
"""
text.pack(ipady= 30)
scroll.pack(ipady=35)
e.pack()
b1.pack()
"""
root.mainloop()
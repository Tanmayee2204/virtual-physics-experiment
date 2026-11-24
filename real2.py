import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import functions

W1=[0,50,100,150,200]
P1=[]
mu1=[]
for i in range(22,51,1):
    P1.append(i)

def MUFinder(We1, Pa1):
    mu=(19+Pa1)/(205+We1)
    mu=round(mu,4)
    return mu
for i in W1:
    if i == W1[0]:
        for k in range(0,6):
            mu1.append(MUFinder(i,P1[k]))
    elif i==W1[1]:
        for k in range(6,16):
            mu1.append(MUFinder(i,P1[k]))
    elif i==W1[2]:
        for k in range(16,23):
            mu1.append(MUFinder(i,P1[k]))
    elif i==W1[3]:
        for k in range(23,28):
            mu1.append(MUFinder(i,P1[k]))
    else:
        mu1.append(MUFinder(i,P1[28]))


#MU Finder


# Trackers for objects in Pan and Block
pan_items = []
block_items = []
# Function to update labels dynamically

def frame_finder():
    pan_t=sum(pan_items)
    block_t=sum(block_items)
    frame=1
    for i in W1:
        if i == block_t and i ==W1[0]:
            for k in range(0,6):
                if pan_t==P1[k]:
                    frame=50
                elif pan_t>=28:
                    frame=480
        elif i == block_t and i==W1[1]:
            for k in range(6,16):
                if pan_t==P1[k]:
                    frame=50
                elif pan_t>=38:
                    frame=480
        elif i == block_t and i==W1[2]:
            for k in range(16,23):
                if pan_t==P1[k]:
                    frame=50
                elif pan_t>=45:
                    frame=480
        elif i == block_t and i==W1[3]:
            for k in range(23,28):
                if pan_t==P1[k]:
                    frame=50
                elif pan_t>=50:
                    frame=480
        elif i == block_t and i==W1[4]:
            if pan_t==50:
                frame=50
            elif pan_t>=51:
                frame=480
    return frame

def update_labels():
    pan_total = sum(pan_items)
    block_total = sum(block_items)
    pan_label.config(text=f"Weights in Pan: {pan_items} | Total: {pan_total}")
    block_label.config(text=f"Weights on Block: {block_items} | Total: {block_total}")

def on_submit():
    frame=frame_finder()
    if frame==50:
        global anim
        anim = animation.FuncAnimation(fig, update, frames=frame, interval=0.001,repeat=False, blit=False)
        canvas.draw_idle()
        error_label.config(text="")
    elif frame==480:
        update(480)
        canvas.draw_idle()
        error_label.config(text="")
    else:
        update(0)
        canvas.draw_idle()
        error_label.config(text="Condition not met,No movement.")

   

def on_reset():
    pan_items.clear()
    block_items.clear()
    update_labels()
    update(0) 
    canvas.draw_idle() 
    status_label.config(text="Reset successfully!")
    error_label.config(text="")
    


# Function to handle adding items
def on_add(destination):
    try:
        selected_value = int(dropdown_var.get())
        if destination == "Pan":
            pan_items.append(selected_value)
        elif destination == "Block":
            block_items.append(selected_value)
        status_label.config(text="Added successfully!")
    except ValueError:
        status_label.config(text="Please select a valid weight!")
    
    #status_label.config(text=("weight is adding in the pan wait..."))

    update_labels()

# Function to handle removing items
def on_remove(destination):
    try:
        selected_value = int(dropdown_var.get())
        if destination == "Pan" and selected_value in pan_items:
            pan_items.remove(selected_value)
        elif destination == "Block" and selected_value in block_items:
            block_items.remove(selected_value)
        status_label.config(text="Removed successfully!")
    except ValueError:
        status_label.config(text="Please select a valid weight!")
    
    update_labels()


# Cylinder class for animation
class Cylinder:
    def __init__(self, x, y, radius, height, color, name, text):
        self.x = x
        self.y = y
        self.radius = radius
        self.height = height
        self.color = color
        self.name = name
        self.text = text

    def draw(self, canvas):
        # Draw top ellipse
        top_ellipse = patches.Ellipse(
            (self.x, self.y),
            self.radius * 2,
            self.radius * 2 / 2,
            linewidth=2,
            edgecolor="black",
            facecolor=self.color,
        )
        canvas.add_patch(top_ellipse)

        # Draw bottom ellipse
        bottom_ellipse = patches.Ellipse(
            (self.x, self.y - self.height),
            self.radius * 2,
            self.radius * 2 / 2,
            linewidth=2,
            edgecolor="black",
            facecolor=self.color,
        )
        canvas.add_patch(bottom_ellipse)

         # Draw connecting lines (sides of the cylinder)
        canvas.plot(
            [self.x - self.radius, self.x - self.radius],
            [self.y, self.y - self.height],
            color="black",
            linewidth=2,
        )
        canvas.plot(
            [self.x + self.radius, self.x + self.radius],
            [self.y, self.y - self.height],
            color="black",
            linewidth=2,
        )


        # Add text
        canvas.text(
            self.x,
            self.y + self.height / 2,
            self.text,
            ha="center",
            va="center",
            color="black",
            fontsize=10,
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


# Update function for animation
def update(frame):
    ax.clear()
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1000)

   # GLASS SURFACE
    glass_surface = patches.Rectangle((50, 400), 900, 40, linewidth=3, edgecolor='skyblue', facecolor='lightblue')  # (x, y), width, height, properties
    ax.add_patch(glass_surface)

    # WOODEN BLOCK (moving horizontally)
    wooden_block_x = 119 + frame  # x position changes with frame
    wooden_block = patches.Rectangle((wooden_block_x, 440), 300, 100, linewidth=3, edgecolor='saddlebrown', facecolor='peru')  # (x, y), width, height, properties
    ax.add_patch(wooden_block)

    # PULLEY LINE
    ax.plot([950, 1050], [420, 480], color='black', linewidth=3)  # (x1, y1), (x2, y2), color, linewidth

    # PULLEY
    pulley = patches.Circle((1050, 480), 35, linewidth=2, edgecolor='black', facecolor='white')  # (x, y), radius, properties
    ax.add_patch(pulley)

    # STRING 1 (moving horizontally)
    string1_x_end = 420 + frame  # x position changes with frame
    ax.plot([string1_x_end, 1050], [515, 515], color='black', linewidth=3)

    # STRING 2 (moving vertically)
    string2_y_end = 250 - frame  # y position changes with frame
    ax.plot([1085, 1085], [480, string2_y_end], color='black', linewidth=3)

    # PAN STRING 1 (moving vertically)
    ax.plot([1085, 990], [string2_y_end, string2_y_end - 50], color='black', linewidth=3)

    # PAN STRING 2 (moving vertically)
    ax.plot([1085, 1180], [string2_y_end, string2_y_end - 50], color='black', linewidth=3)

    #ax.plot([990,1180],[string2_y_end-50, string2_y_end-50], linestyle='dotted', color='black', linewidth=2)

    # PAN (moving vertically)
    arc_y = 200 - frame  # y position changes with frame
    arc = patches.Arc((1085, arc_y), 190, 100, theta1=180, theta2=360, linewidth=3, color='orange')
    ax.add_patch(arc)

    # Draw weight in pan if total > 0
    if sum(pan_items) > 0:
        weight_circle = patches.Circle((1085, arc_y-18 ), 30, linewidth=2, edgecolor='black', facecolor='grey')
        ax.add_patch(weight_circle)
    elif sum(pan_items)==0:
        weight_circle = patches.Circle((1085, arc_y-10 ), 30, linewidth=2, edgecolor='white', facecolor='white')
        ax.add_patch(weight_circle)


    weight_x=129+frame
    for i in range(len(block_items)):
        if(i<=2):
            weights = patches.Rectangle((weight_x , 550), 30, 10, linewidth=3, edgecolor='saddlebrown', facecolor='peru')  # (x, y), width, height, properties
            ax.add_patch(weights)
            weight_x+=100
        elif(i>2):
            weights = patches.Rectangle((weight_x , 550), 30, 10, linewidth=3, edgecolor='white', facecolor='white')  # (x, y), width, height, properties
            ax.add_patch(weights)
            weight_x+=100


    # Cylinder animation
    for cylinder in cylinders:
       # cylinder.move(-10, 0)  # Move cylinders leftwards
        cylinder.draw(ax)

    # Update the canvas
    canvas.draw_idle()


# Create the main application window
root = tk.Tk()
root.title("Coefficient of static friction")
root.geometry("1000x1000")
root.state("zoomed")
# Left frame for controls
left_frame = tk.Frame(root, border=5, borderwidth=5 ,height=1000,width=1000)
left_frame.pack(side=tk.LEFT, padx=100, pady=100,)

# Dropdown options
options = [0, 1, 2, 5, 10, 15, 20, 50, 100, 100]

# Dropdown variable
dropdown_var = tk.StringVar(value="Select Weight")
dropdown = ttk.Combobox(left_frame, textvariable=dropdown_var)
dropdown['values'] = options
dropdown.grid(row=0, column=1, padx=10, pady=10)

# Labels for Select Action and Destination
action_label = tk.Label(left_frame, text="Select Action:")
action_label.grid(row=1, column=0, padx=10, pady=5)

destination_label = tk.Label(left_frame, text="Select Destination:")
destination_label.grid(row=2, column=0, padx=10, pady=5)

# Add buttons for actions
add_pan_button = tk.Button(left_frame, text="Add Pan", width=10, command=lambda: on_add("Pan"))
add_pan_button.grid(row=1, column=1, padx=10, pady=5)

add_block_button = tk.Button(left_frame, text="Add Block", width=10, command=lambda: on_add("Block"))
add_block_button.grid(row=1, column=2, padx=10, pady=5)

# Remove buttons for actions
remove_pan_button = tk.Button(left_frame, text="Remove Pan", width=10, command=lambda: on_remove("Pan"))
remove_pan_button.grid(row=2, column=1, padx=10, pady=5)

remove_block_button = tk.Button(left_frame, text="Remove Block", width=10, command=lambda: on_remove("Block"))
remove_block_button.grid(row=2, column=2, padx=10, pady=5)

# Submit button
submit_button = tk.Button(left_frame, text="Submit", width=12, command=on_submit)
submit_button.grid(row=3, column=1, pady=10)

#Reset Button
reset_button = tk.Button(left_frame, text="Reset", width=12, command=on_reset)
reset_button.grid(row=3, column=2,  pady=10)

# Labels to display the state of Pan and Block
pan_label = tk.Label(left_frame, text="Weights in Pan: [] | Total: 0", fg="blue")
pan_label.grid(row=4, column=0, columnspan=3, pady=5)

block_label = tk.Label(left_frame, text="Weights on Block: [] | Total: 0", fg="green")
block_label.grid(row=5, column=0, columnspan=3, pady=5)

# Status label
status_label = tk.Label(left_frame, text="", fg="red")
status_label.grid(row=6, column=0, columnspan=3, pady=5)

error_label = tk.Label(left_frame, text="", fg="red")
error_label.grid(row=10, column=0, columnspan=3, pady=5)

# Right frame for animation
right_frame = tk.Frame(root,border=5,borderwidth=5,height=1000,width=1000)
right_frame.pack(side=tk.RIGHT, padx=1, pady=1)

# Matplotlib figure and canvas for animation
fig, ax = plt.subplots(figsize=(15, 8))
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Create cylinders
cylinder0 = Cylinder(1800, 950, 20, 20, "lightblue","block0","1g")
cylinder1 = Cylinder(1800, 870, 25, 35, "red","block1","2g")
cylinder2 = Cylinder(1800, 770, 35, 45, "blue","block2","5g")
cylinder3 = Cylinder(1800, 650, 45, 55, "green","block3","10g")
cylinder4 = Cylinder(1800, 500, 50, 65, "brown", "block4","20g")
cylinder5 = Cylinder(1800, 350, 55, 75, "orange", "block5","50g")
cylinder6 = Cylinder(1800, 150, 65, 85, "purple", "block6","100g")
cylinders = [cylinder0, cylinder1, cylinder2, cylinder3, cylinder4,cylinder5, cylinder6]

def on_closing():
    root.destroy()
    root.quit()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Create animation
frames=frame_finder()

ani = animation.FuncAnimation(fig, update,frames=frames, interval=10,repeat=False, blit=False)

# if frames==50:
#     ani = animation.FuncAnimation(fig, update, frames=frames, interval=0.001,repeat=False, blit=False)
# elif frames==480:
#     ani = animation.FuncAnimation(fig, update, frames=frames, interval=0.001,repeat=False, blit=False)
# Start the Tkinter event loop
root.mainloop()

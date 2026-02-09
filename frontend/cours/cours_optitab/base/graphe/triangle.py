import matplotlib.pyplot as plt
import ternary

# Set up the figure and axes
fig, tax = ternary.figure(scale=180)
fig.set_size_inches(8, 7)

# Draw the boundary and grid lines
tax.boundary(linewidth=2.0)
tax.gridlines(color="black", multiple=30, linewidth=0.5)

# Set the title of the graph
tax.set_title("Graph of Triangle Angles: Â + B̂ + Ĉ = 180°\n", fontsize=16, fontweight='bold')

# Label the corners of the ternary plot
# These represent the theoretical maximum of 180 degrees for a single angle
tax.left_corner_label("B̂ (0, 180, 0)", fontsize=12, offset=0.14)
tax.right_corner_label("Ĉ (0, 0, 180)", fontsize=12, offset=0.14)
tax.top_corner_label("Â (180, 0, 0)", fontsize=12, offset=0.16)

# Add points for specific types of triangles
# Equilateral triangle: all angles are 60 degrees
equilateral_point = (60, 60, 60)
tax.scatter([equilateral_point], marker='o', color='blue', s=100, label='Equilateral (60°, 60°, 60°)')

# Right-isosceles triangle: one angle is 90, the other two are 45
right_isosceles_point = (90, 45, 45)
tax.scatter([right_isosceles_point], marker='s', color='red', s=100, label='Right-Isosceles (90°, 45°, 45°)')

# Obtuse-isosceles triangle: one angle is 120, the other two are 30
obtuse_isosceles_point = (120, 30, 30)
tax.scatter([obtuse_isosceles_point], marker='^', color='green', s=100, label='Obtuse-Isosceles (120°, 30°, 30°)')

# Add a legend
tax.legend(fontsize=10, loc='upper right', bbox_to_anchor=(1.1, 1))

# Clean up the plot
tax.clear_matplotlib_ticks()
tax.get_axes().axis('off')

# Show the plot
plt.show()
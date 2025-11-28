import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


P = [
    [0.7, 0.2, 0.1],
    [0.3, 0.4, 0.3],
    [0.2, 0.3, 0.5]
]


def mat_mult_vec(vec, mat):
    """Computes the multiplication of a row vector by a matrix (v * P)."""
    result = [0, 0, 0]
    for j in range(3):
        result[j] = vec[0]*mat[0][j] + vec[1]*mat[1][j] + vec[2]*mat[2][j]
    return result

def mat_power(mat, n):
    """Computes the matrix P raised to the power n (P^n). (Not used in core compute, but kept for completeness)."""
    
    # Identity matrix
    res = [[1 if i==j else 0 for j in range(3)] for i in range(3)]
    temp = [row[:] for row in mat]
    for _ in range(n):
        res = mat_mult_mat(res, temp)
    return res

def mat_mult_mat(A, B):
    """Computes the multiplication of two 3x3 matrices (A * B)."""
    
    C = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                C[i][j] += A[i][k]*B[k][j]
    return C

def normalize(vec):
    """Normalizes a vector so its elements sum to 1."""
    
    s = sum(vec)
    if s == 0: return vec
    return [v/s for v in vec]

def compute(v0, years):
    """Computes the market share vector after 'years' iterations: v_years = v0 * P^years."""
    
    result = v0[:]
    for _ in range(years):
        result = mat_mult_vec(result, P)
    return normalize(result)

def steady_state():
    """Computes the steady-state vector (eigenvector corresponding to eigenvalue 1)."""
    
    v = [1/3, 1/3, 1/3]  # Start with uniform distribution
    for _ in range(1000): # Max iterations for convergence
        v_next = mat_mult_vec(v, P)
        # Check for convergence
        if all(abs(v_next[i] - v[i]) < 1e-10 for i in range(3)):
            break
        v = v_next
    return normalize(v)

def plot_graph(v0, years):
    """Creates a Matplotlib figure showing the evolution of market shares over time."""
    
    shares = [v0[:]]
    current = v0[:]
    for _ in range(years):
        current = mat_mult_vec(current, P)
        shares.append(current[:])

    x_vals = list(range(years+1))
    xs = [s[0] for s in shares]
    ys = [s[1] for s in shares]
    zs = [s[2] for s in shares]

    # --- Matplotlib Pure Black Theme Settings ---
    plt.style.use('dark_background')
    
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']

    fig, ax = plt.subplots(figsize=(7, 4))
    
    # Plot data with distinct, bright colors
    ax.plot(x_vals, xs, marker="o", label="X", color="#00FFFF", linewidth=2.5) # Cyan
    ax.plot(x_vals, ys, marker="s", label="Y", color="#FFFF00", linewidth=2.5) # Yellow
    ax.plot(x_vals, zs, marker="^", label="Z", color="#FF00FF", linewidth=2.5) # Magenta

    ax.set_title("Market Share Evolution", fontsize=16, color='white')
    ax.set_xlabel("Years", fontsize=12, color='white')
    ax.set_ylabel("Market Share", fontsize=12, color='white')
    
    # Legend with slightly visible background
    ax.legend(fontsize=10, frameon=True, facecolor='#111111', edgecolor='#CCCCCC')
    
    # Grid and axis styling
    ax.grid(True, linestyle='--', alpha=0.5, color='#333333')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    # Set backgrounds to pure black
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('black') 

    fig.tight_layout()

    return fig


def on_compute():
    """Handles the button click event, performs calculations, updates results, and plots the graph."""
    try:
        # Get and validate initial shares
        v0 = [float(e_x.get()), float(e_y.get()), float(e_z.get())]
        s = sum(v0)
        if abs(s - 1.0) > 1e-6:
            messagebox.showwarning("Warning", "Initial shares do not sum to 1. They will be normalized.")
            v0 = normalize(v0)

        years = int(sp_years.get())
        
        # Perform Markov Chain calculations
        vN = compute(v0, years)
        pi = steady_state()

        label_vN.config(text=f"Shares after {years} years:")

        # Update result labels
        for i, val in enumerate(vN):
            labels_result[i]['text'] = f"{val:.6f}"
        for i, val in enumerate(pi):
            labels_ss[i]['text'] = f"{val:.6f}"

        # Clear old graph
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Plot new graph
        fig = plot_graph(v0, years)
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as ex:
        messagebox.showerror("Error", f"Invalid Input: {str(ex)}")


# --- GUI Setup ---
root = tk.Tk()
root.title("PGM ISE: Market Share Predictor (X, Y, Z)")
root.state("zoomed")
root.configure(bg='black') # Pure black root background

# --- Pure Black Theme Styles ---
style = ttk.Style()
style.theme_use('clam') 

# Configure styles for a pure black theme
TEXT_COLOR = 'white'
ACCENT_COLOR = '#00FFFF' # Cyan accent
BACKGROUND_COLOR = 'black'
ELEMENT_BG = '#1A1A1A' # Very dark gray for elements like matrix entries and entry fields

style.configure('.', background=BACKGROUND_COLOR, foreground=TEXT_COLOR, font=("Arial", 12))
style.configure('TFrame', background=BACKGROUND_COLOR)
style.configure('TLabel', background=BACKGROUND_COLOR, foreground=TEXT_COLOR, font=("Arial", 12))
style.configure('TButton', background=ACCENT_COLOR, foreground='black', font=("Arial", 12, "bold"), relief='flat')
style.map('TButton', background=[('active', '#00DDDD')]) # Slightly lighter accent on hover
style.configure('TEntry', fieldbackground=ELEMENT_BG, foreground=TEXT_COLOR, font=("Arial", 12), borderwidth=0)
style.configure('TSpinbox', fieldbackground=ELEMENT_BG, foreground=TEXT_COLOR, font=("Arial", 12), borderwidth=0)
style.configure('TSeparator', background='#333333')

# Custom style for bold labels
style.configure("Bold.TLabel", font=("Arial", 12, "bold"))


main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# Left Side: Input and Results
input_frame = ttk.Frame(main_frame, style='TFrame')
input_frame.pack(side="left", fill="y", padx=20, pady=10)

row_count = 0

# --- Input Section ---
ttk.Label(input_frame, text="Initial share X:", style='TLabel').grid(row=row_count, column=0, sticky="e", pady=5); row_count += 1
ttk.Label(input_frame, text="Initial share Y:", style='TLabel').grid(row=row_count, column=0, sticky="e", pady=5); row_count += 1
ttk.Label(input_frame, text="Initial share Z:", style='TLabel').grid(row=row_count, column=0, sticky="e", pady=5); row_count += 1

e_x = ttk.Entry(input_frame, width=10, style='TEntry'); e_x.insert(0,"0.5"); e_x.grid(row=row_count-3, column=1, pady=5)
e_y = ttk.Entry(input_frame, width=10, style='TEntry'); e_y.insert(0,"0.3"); e_y.grid(row=row_count-2, column=1, pady=5)
e_z = ttk.Entry(input_frame, width=10, style='TEntry'); e_z.insert(0,"0.2"); e_z.grid(row=row_count-1, column=1, pady=5)

ttk.Label(input_frame, text="Years:", style='TLabel').grid(row=row_count, column=0, sticky="e", pady=5)
sp_years = ttk.Spinbox(input_frame, from_=0, to=100, width=10, style='TSpinbox'); sp_years.set("5"); sp_years.grid(row=row_count, column=1, pady=5); row_count += 1

ttk.Button(input_frame, text="Compute & Show Graph", command=on_compute).grid(row=row_count, column=0, columnspan=2, pady=(15,15)); row_count += 1

ttk.Separator(input_frame, orient="horizontal").grid(row=row_count, column=0, columnspan=2, sticky="ew", pady=10); row_count += 1

# --- Transition Matrix Section ---
ttk.Label(input_frame, text="Transition Matrix P:", style='Bold.TLabel', font=("Arial", 14, "bold")).grid(row=row_count, column=0, columnspan=2, pady=(5,5)); row_count += 1
matrix_frame = ttk.Frame(input_frame, style='TFrame')
matrix_frame.grid(row=row_count, column=0, columnspan=2, pady=(0, 10)); row_count += 1

# Display P matrix
for i, label in enumerate(["X", "Y", "Z"]):
    ttk.Label(matrix_frame, text=label, style='Bold.TLabel').grid(row=0, column=i+1, padx=5) 

for r in range(3):
    ttk.Label(matrix_frame, text=["X", "Y", "Z"][r], style='Bold.TLabel').grid(row=r+1, column=0, sticky="e")
    for c in range(3):
        val = P[r][c]
        # Use a distinct background for matrix entries
        lbl_mat = ttk.Label(matrix_frame, text=f"{val:.1f}", background=ELEMENT_BG, foreground=TEXT_COLOR, padding=(5,2))
        lbl_mat.grid(row=r+1, column=c+1, padx=5, pady=2)


ttk.Separator(input_frame, orient="horizontal").grid(row=row_count, column=0, columnspan=2, sticky="ew", pady=10); row_count += 1

# --- Results Section ---
label_vN = ttk.Label(input_frame, text="Shares after N years:", style='Bold.TLabel')
label_vN.grid(row=row_count, column=0, columnspan=2, pady=(5,5)); row_count += 1

labels_result = []
for i, s in enumerate(["X","Y","Z"]):
    ttk.Label(input_frame, text=f"{s}:", style='TLabel').grid(row=row_count, column=0, sticky="e", pady=5)
    lbl = ttk.Label(input_frame, text="0.000000", style='TLabel', foreground=ACCENT_COLOR) # Highlight results
    lbl.grid(row=row_count, column=1, sticky="w", pady=5)
    labels_result.append(lbl); row_count += 1

ttk.Separator(input_frame, orient="horizontal").grid(row=row_count, column=0, columnspan=2, sticky="ew", pady=10); row_count += 1
ttk.Label(input_frame, text="Long-run steady-state:", style='Bold.TLabel').grid(row=row_count, column=0, columnspan=2, pady=(5,5)); row_count += 1
labels_ss = []
for i, s in enumerate(["X","Y","Z"]):
    ttk.Label(input_frame, text=f"{s}:", style='TLabel').grid(row=row_count, column=0, sticky="e", pady=5)
    lbl = ttk.Label(input_frame, text="0.000000", style='TLabel', foreground=ACCENT_COLOR) # Highlight steady state
    lbl.grid(row=row_count, column=1, sticky="w", pady=5)
    labels_ss.append(lbl); row_count += 1

# Right side: Graph area
graph_frame = ttk.Frame(main_frame, style='TFrame')
graph_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

# Initialize the computation and graph display
on_compute()

root.mainloop()

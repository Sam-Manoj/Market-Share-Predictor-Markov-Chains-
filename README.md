# Market Share Predictor (Tkinter + Markov Chains)

This project is a **Market Share Predictor** built using **Python**, **Tkinter**, and **Matplotlib**. It models the evolution of market shares for three companies **X, Y, Z** using a **Markov Chain transition matrix**.

It provides:

* A Tkinter GUI with a pure-black theme
* Entry fields for initial market shares
* A configurable number of years
* Transition matrix display
* Numerical results for market shares after N years
* Long‑run steady‑state distribution
* A live Matplotlib graph embedded in the UI

---

## 🚀 How the Application Works

### **1. Transition Matrix P**

The system uses a fixed 3×3 Markov transition matrix:

```
P = [
    [0.7, 0.2, 0.1],
    [0.3, 0.4, 0.3],
    [0.2, 0.3, 0.5]
]
```

Each row shows the probability of staying at or switching from a company to another.

---

## **2. Initial Market Shares**

Users provide initial market shares for **X**, **Y**, and **Z**. If they do not sum to 1, the app automatically normalizes the values.

---

## **3. Markov Chain Iteration**

The application computes:

```
vₙ = v₀ * Pⁿ
```

This is done by iterating vector‑matrix multiplication.

### Key functions:

* **mat_mult_vec()** → multiplies vector × matrix
* **compute()** → performs iterations to get vₙ
* **steady_state()** → repeatedly applies P until convergence

---

## **4. Graph Plotting**

Uses **Matplotlib** with a pure‑black cyber theme:

* Cyan, Yellow, and Magenta curves
* Smooth lines with markers
* Dark grid aesthetic
* Embedded into Tkinter via `FigureCanvasTkAgg`

---

## **5. Tkinter GUI**

The UI is split into left and right panels:

### Left Panel

* Input fields
* Transition matrix display
* Computed values
* Steady‑state values

### Right Panel

* Embedded graph showing the evolution of market share

A custom dark theme is implemented using **ttk.Style()**.

---

## 🖼️ Screenshot

Below is a PNG preview of the interface:

**PNG Screenshot:**
(ss.png)

---

## 📌 How to Run

1. Install the required packages:

```
pip install matplotlib
```

Tkinter comes preinstalled with most Python distributions.

2. Save the script as `market_share_predictor.py`.

3. Run the application:

```
python market_share_predictor.py
```

---

## 💡 Notes

* The Markov model assumes market shares depend only on the previous year (memoryless process).
* The steady‑state value represents the long‑run expected market distribution.
* Style and color choices are optimized for a dark theme.

---

If you'd like, I can also generate a PDF version, add more visualizations, or modularize the code!

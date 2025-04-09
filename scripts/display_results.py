import matplotlib.pyplot as plt

# Coordenadas de GCPs
gcp_labels = ["GCP1", "GCP2", "GCP4", "GCP3"]
x = [0, 20, 20, 0]
y = [0, 0, 20, 20]

# Crear figura
plt.figure(figsize=(6, 6))
plt.plot(x + [x[0]], y + [y[0]], 'b-')  # cerrar el cuadrado
plt.scatter(x, y, color='red')

# Etiquetas
for xi, yi, label in zip(x, y, gcp_labels):
    plt.text(xi + 0.5, yi + 0.5, label, fontsize=12)

plt.grid(True)
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.title("Ground Control Points (GCPs)")
plt.axis('equal')
plt.show()

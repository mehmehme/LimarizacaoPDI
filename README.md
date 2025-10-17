<h1 align="center">🌀 Limiarização PDI 🧠</h1>

<p align="center">
  <img src="https://media.tenor.com/ShEbPnHs2lIAAAAM/looking-for-something-om-nom.gif" alt="Om Nom GIF">
</p>

---

## 📸 Sobre o projeto
Este projeto implementa **limiarização (thresholding)** em imagens usando **OpenCV** e uma interface de controle dinâmica.  
A ideia é visualizar, em tempo real, como o valor de limiar (`thresh`) e o tipo de threshold afetam a imagem processada.

---

## ⚙️ Tecnologias usadas
- 🐍 **Python 3**
- 🧠 **OpenCV (cv2)**
- 🪟 Módulo `window` personalizado para interface interativa

---

## 🚀 Como executar

1. **Clone o repositório**
   ```bash
   git clone https://github.com/mehmehme/LimarizacaoPDI.git
   cd LimarizacaoPDI
   ```
Instale as dependências

```bash
pip install opencv-python
```

(Opcional) Para funções extras:

```bash
pip install opencv-contrib-python
```

Execute o programa

bash
Copiar código
python main.py
🎛️ Controles
Controle	Função
Thresh	Define o valor de limiar
Max Value	Valor máximo aplicado nos pixels acima do limiar
Type	Escolhe o tipo de limiarização (Binary, ToZero, etc.)

O tipo atual é mostrado na imagem durante a execução 💫

🧩 Tipos de Limiarização
Tipo	Descrição
THRESH_BINARY	Pixels ≥ thresh → maxval
THRESH_BINARY_INV	Pixels ≥ thresh → 0
THRESH_TRUNC	Pixels > thresh → thresh
THRESH_TOZERO	Pixels < thresh → 0
THRESH_TOZERO_INV	Pixels > thresh → 0

💡 Exemplo de código principal
python
Copiar código
retval, img = cv2.threshold(image, thresh, maxval, ttype)


import cv2
import window
from cv2.typing import MatLike

window.CONTROL_NAME = ["Thresh", "Max Value", "Type", "Unused"]
window.MAXIMUM_VALUES = [255, 255, 4, 0]
window.MINIMUM_VALUES = [0, 0, 0, 0]

THRESH_TYPES = {
    0: "THRESH_BINARY",
    1: "THRESH_BINARY_INV",
    2: "THRESH_TRUNC",
    3: "THRESH_TOZERO",
    4: "THRESH_TOZERO_INV"
}

def load_image() -> MatLike | None:
    image = cv2.imread("digital.png",cv2.IMREAD_GRAYSCALE)
    return image


def change_control(image: MatLike, thresh: int, maxval: int, ttype: int, _: int) -> MatLike:
    retval, img = cv2.threshold(image,thresh,maxval,ttype)
    
    type_name = THRESH_TYPES.get(ttype, "Unknown")

    # Adiciona o nome na imagem
    cv2.putText(
        image,
        f"Tipo: {type_name}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )
    
    return img



window.load_image = load_image
window.change_control = change_control
window.show()


# digital.png usamos thresh_binary max value em 255 e tresh 150
# bolhas.png é bom thresh_tozero com max em 240 e thresh 194
# pac.png é bom o thresh_binary com thresh 148 e max 207
# pac2.png usamos thresh_binary thresh 85 e max 255
# star.png usamos thresh_binary thresh 118 e max 255
# bacilos focando a estrutura alongada thresh_binary thresh 63 max 255
# bacilos focando nas estruturas claras thresh_binary_inv thresh 122 max 248
# bacilos com as estruturas diferenciadas thresh_to_zero thresh 66 max 0
# para as montanhas usamos thresh_to zero thresh 124 e max 0 

# a limiarização funcionou bem até as estruturas alongadas do bacilo, após isso as imagens
# são limiarizadas, mas ficam acinzentadas precisando algum tratamento ou aplicação de filtro para consertá-las
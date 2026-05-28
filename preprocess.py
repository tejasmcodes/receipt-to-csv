import cv2
from deskew import determine_skew

def preprocess_image(img_path):

    img = cv2.imread(img_path)
    original = img.copy()

    # None -> No Hard fixed sizes, scales the image by a factor of 2(x,y)
    # interpolation is applied to get smoothen and sharp the edge of the enlarges text
    # because small text causes OCR engine to fail
    scaled = cv2.resize(
        original, 
        None, 
        fx=2.0, 
        fy=2.0 , 
        interpolation = cv2.INTER_CUBIC
        )
    

    # convert to grayscale, because OCR engines struggles with RGB
    grayscale = cv2.cvtColor(
        scaled, 
        cv2.COLOR_BGR2GRAY
        )

    # deskewing
    angle = determine_skew(grayscale)
    if abs(angle)<10:

        (h, w) = grayscale.shape
        center = (w//2, h//2)

        M = cv2.getRotationMatrix2D(
                                    center, 
                                    angle, 
                                    1.0
                                    )


        processed_img = cv2.warpAffine(
                                grayscale, 
                                M, 
                                (w, h), 
                                flags=cv2.INTER_CUBIC, 
                                borderMode=cv2.BORDER_REPLICATE
                                )

    else:
        processed_img=  grayscale

    return processed_img

if __name__ == "__main__":
    import os
    preprocessed_image = preprocess_image("samples/s7.png")
    output_dir = "outputs/preprocessed"
    output_path = os.path.join(output_dir, "s7.png")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cv2.imwrite(output_path, preprocessed_image)
    print(f"Successfully saved the preprocessed image to: {output_path}")

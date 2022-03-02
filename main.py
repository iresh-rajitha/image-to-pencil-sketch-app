# This is a sample Python script.
import base64
from io import BytesIO

import streamlit as st
import cv2
import numpy as np
from PIL import Image

import matplotlib.pyplot as plt


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_image_download_link(img):
    """Generates a link allowing the PIL image to be downloaded
    in:  PIL image
    out: href string
    """
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}" download ="result.jpg">Download result</a>'
    return href


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    st.title("CONVERT IMAGE INTO A COLOR PENCIL SKETCH")
    st.header("Upload your file")
    # color = st.color_picker('Pick A Color', '#00f900')
    # st.write('The current color is', color)
    uploaded_file = st.file_uploader("Choose a image file", type=['png', 'jpg'])

    if uploaded_file is not None:
        # Convert the file to an opencv image.

        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        # Now do something with the image! For example, let's display it:
        st.image(uploaded_file)

        grey_img = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)

        # Invert Image
        invert_img = cv2.bitwise_not(grey_img)
        # invert_img=255-grey_img

        # Blur image
        blur_img = cv2.GaussianBlur(invert_img, (111, 111), 0)

        # Invert Blurred Image
        invblur_img = cv2.bitwise_not(blur_img)
        # invblur_img=255-blur_img

        # Sketch Image
        sketch_img = cv2.divide(grey_img, invblur_img, scale=256.0)

        dst_sketch, dst_color_sketch = cv2.pencilSketch(opencv_image, sigma_s=50, sigma_r=0.07, shade_factor=0.08)
        dst_water_color = cv2.stylization(opencv_image, sigma_s=50, sigma_r=0.0825)
        invert = cv2.bitwise_not(dst_sketch)

        option = st.selectbox(
            'Choose Your Preferred pattern',
            ('Pencil Sketch', 'Color Pencil', 'Water Color', 'Final Sketch'))

        if option == "Pencil Sketch":
            option = st.selectbox('Choose Your Preferred Color', ('Grey', 'Red', 'Green', 'Blue', 'Purple'))
            fig = plt.figure(figsize=(12, 5))
            img = plt.imshow(invert, cmap=option + 's'), plt.axis('off'), plt.title('Pencil-Sketch in ' + option,
                                                                                    size=20)
            st.pyplot(fig)
            # plt.imsave(img,fig)
            result = Image.fromarray(invert)
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)

        # result = Image.fromarray(img)
        # st.markdown(get_image_download_link(result), unsafe_allow_html=True)

        if option == "Color Pencil":
            fig = plt.figure(figsize=(12, 5))
            result = cv2.cvtColor(dst_color_sketch, cv2.COLOR_BGR2RGB)
            plt.imshow(result), plt.axis('off'), plt.title(
                'Color Pencil-Sketch', size=20)
            st.pyplot(fig)
            result = Image.fromarray(result)
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)

        if option == "Water Color":
            fig = plt.figure(figsize=(12, 5))
            result = cv2.cvtColor(dst_water_color, cv2.COLOR_BGR2RGB)
            plt.imshow(result), plt.axis('off'), plt.title(
                'Water Color Image', size=20)
            st.pyplot(fig)
            result = Image.fromarray(result)
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)

        if option == "Final Sketch":
            st.image(sketch_img)
            result = Image.fromarray(sketch_img)
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)

        # st.header("Data Application")

        # Save Sketch
        # cv2.imwrite('sketch.png', sketch_img)
        print('Hello1')
        # st.image(invert, cmap='Purples')
        # st.image(newimage)

        # st.download_button('Download binary file', sketch_img)
        img_file = "test"
        result = Image.fromarray(sketch_img)
        # st.markdown(get_image_download_link(result, img_file, 'Download ' + img_file), unsafe_allow_html=True)
        # st.image(result, caption=f"Image Predicted")
        # result = Image.fromarray(result)

        # st.markdown(get_image_download_link(result), unsafe_allow_html=True)

        # st.download_button('Download CSV', result, 'file/jpg')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
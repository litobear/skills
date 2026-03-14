import argparse
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

def generate_image(output_file: str, prompt: str):
    vertexai.init()

    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        seed=1,
        add_watermark=False,
    )

    images[0].save(location=output_file)
    return images

# 範例執行
generate_image(
    output_file="image_2026-03-12-15-00-43.jpeg",
    prompt="兔子跳高高",
)
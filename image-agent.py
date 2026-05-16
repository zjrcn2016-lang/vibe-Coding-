from openai import OpenAI
import os
import sys
import subprocess
import requests
from PIL import Image
from io import BytesIO
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Lib"))

API_KEY = os.getenv("ZHIPU_API_KEY", "977abc8921f94ddfb5a04a8a5eb9e8df.eXbUL6z8BkdTdBX4")
MODEL_NAME = "glm-4"
OUTPUT_DIR = "generated_images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

def generate_image(prompt: str, size: str = "1024x1024") -> Image.Image:
    print(f">>> 正在生成图片：{prompt[:50]}...")

    try:
        response = client.images.generate(
            model="cogview-3",
            prompt=prompt,
            size=size
        )

        image_url = response.data[0].url
        img_response = requests.get(image_url)
        return Image.open(BytesIO(img_response.content))

    except Exception as e:
        raise Exception(f"生成失败：{str(e)}")

def save_image(image: Image.Image, filename: str = None) -> tuple:
    if filename is None:
        from datetime import datetime
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    image.save(filepath)
    return filepath, filename

def open_folder():
    subprocess.Popen(f'explorer "{os.path.abspath(OUTPUT_DIR)}"')
    return f"已打开文件夹: {OUTPUT_DIR}"

def run_cli():
    print("[Image] 智谱图片生成Agent (命令行模式)\n")

    prompt = input("请输入图片描述（英文更好）：\n> ")

    if not prompt.strip():
        print("提示词不能为空！")
    else:
        print(f"\n正在生成图片：{prompt}\n")
        try:
            img = generate_image(prompt)
            filepath, filename = save_image(img)
            print(f"[OK] 图片已保存：{filepath}")
            img.show()
        except Exception as e:
            print(f"[ERROR] 生成失败：{str(e)}")

def run_gradio():
    import gradio as gr

    with gr.Blocks(title="Image Generator") as app:
        gr.Markdown("# Image Generator")
        gr.Markdown("基于智谱 CogView-3 模型的图片生成工具")

        with gr.Row():
            with gr.Column(scale=3):
                prompt_input = gr.Textbox(
                    label="图片描述 (Prompt)",
                    placeholder="输入图片描述，如: A cute cat sitting on a sofa",
                    lines=3
                )
                size_options = gr.Dropdown(
                    label="图片尺寸",
                    choices=["1024x1024", "768x1024", "1024x768"],
                    value="1024x1024"
                )
                with gr.Row():
                    generate_btn = gr.Button("生成图片", variant="primary")
                    open_btn = gr.Button("打开文件夹", icon="📁")

            with gr.Column(scale=2):
                output_image = gr.Image(label="生成结果", type="pil")

        status_text = gr.Textbox(label="状态", interactive=False, lines=1)

        def generate_and_save(prompt, size):
            if not prompt.strip():
                return None, "提示词不能为空！"
            try:
                img = generate_image(prompt, size)
                filepath, filename = save_image(img)
                return img, f"已保存: {filename}"
            except Exception as e:
                return None, f"生成失败: {str(e)}"

        generate_btn.click(
            fn=generate_and_save,
            inputs=[prompt_input, size_options],
            outputs=[output_image, status_text]
        )

        open_btn.click(fn=open_folder, outputs=status_text)

    app.launch(share=False)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        run_gradio()
    else:
        run_cli()
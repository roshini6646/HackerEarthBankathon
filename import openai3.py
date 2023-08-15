import openai
import gradio
import pytesseract
from PIL import Image

# Set your OpenAI API key
openai.api_key = "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"

# Initial message from the system
messages = [{"role": "system", "content": "You are HR for job interview "}]

# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return str(e)

# Main function for the virtual HR assistant
def CustomChatGPT(image, make_improvements):
    # Extract text from the provided image
    job_description = extract_text_from_image(image.name)
    
    # If text extraction fails, return an error message
    if not job_description:
        return "Failed to extract text from the image. Please provide a clear image with readable text."
    
    # Append user's job description to the messages
    messages.append({"role": "user", "content": "Job Description: " + job_description})
    
    # Get assistant's feedback on the job description
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    feedback = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": feedback})
    
    # Check if the user wants to make improvements
    if make_improvements.lower() == "yes":
        # Ask the assistant for improvements to the job description
        messages.append({"role": "user", "content": "Please suggest improvements to the job description."})
        
        # Get assistant's suggestions for improvements
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        improvements = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": improvements})
        
        # Return the assistant's suggestions for improvements
        return improvements
    else:
        # User chose not to make improvements
        return "No improvements will be made to the job description."

try:
    # Create a Gradio interface with an image input and a button input
    image_input = gradio.inputs.Image()
    button_input = gradio.interface.Button(text="Make Improvements?", value="yes")
    demo = gradio.Interface(fn=CustomChatGPT, inputs=[image_input, button_input], outputs="text", title="Virtual HR")
    
    # Launch the Gradio interface
    demo.launch(share=True)
except Exception as e:
    print("An error occurred:", str(e))


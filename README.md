

<h1>SeeSpeakTranslate_GUI</h1>

<h2>Description</h2>
    <p>
        This project provides a content description application that can analyze frames from real-time video streams, supports multiple languages, and includes text-to-speech (TTS) capabilities. The default generation backend is Ollama (local/hosted). The application analyzes images and delivers descriptions in various languages, which can also be audibly presented. It features a user-friendly interface with customizable style options.
    </p>

<h2>Features</h2>
<ul>
    <li><strong>Real-Time Video Streaming:</strong> View and manage video streams from different camera sources.</li>
    <li><strong>Frame Description:</strong> AI-powered content description that analyzes and describes video frames.</li>
    <li><strong>Multi-Language Support:</strong> Content descriptions in English, Turkish, German, and Arabic.</li>
    <li><strong>Text-to-Speech Conversion:</strong> Listen to descriptions in the selected language.</li>
    <li><strong>User-Friendly Interface:</strong> Intuitive and easy-to-use interface.</li>
    <li><strong>Customizable Style:</strong> Personalize the application's appearance with style settings.</li>
</ul>

<h2>Files and Modules</h2>
<ol>
    <li>
        <strong>content_description.py:</strong>
        <ul>
            <li>Contains the content description class and functions.</li>
            <li>Provides user input handling, frame description, and text-to-speech functionality.</li>
        </ul>
    </li>
    <li>
        <strong>main.py:</strong>
        <ul>
            <li>The main entry point of the application.</li>
            <li>Sets up the user interface using Tkinter and applies style settings.</li>
            <li>Initializes the video stream handler and content describer objects.</li>
        </ul>
    </li>
    <li>
        <strong>video_stream.py:</strong>
        <ul>
            <li>Contains the class that manages video streaming.</li>
            <li>Processes video streams from the camera and displays them on a Tkinter Canvas.</li>
            <li>Provides functions to start, stop, and update the video stream.</li>
        </ul>
    </li>
</ol>

<h2>Usage</h2>
<ol>
    <li>
        <p><strong>Install Required Libraries:</strong></p>
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>
        <p><strong>Ollama (Default) Setup:</strong></p>
        <p>This project expects Ollama as the default generation backend. Configure the following in <code>.env</code> if needed:</p>
        <pre><code>OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=gpt-4o-mini
</code></pre>
        <p>Install the <code>requests</code> package if not already installed: <code>pip install requests</code></p>
    </li>
    <li>
        <p><strong>Run the Application:</strong></p>
        <pre><code>python main.py</code></pre>
    </li>
    <li>
        <p><strong>Select Camera and Language:</strong></p>
        <p>In the application interface, select a camera from the available options and choose the desired description language.</p>
    </li>
    <li>
        <p><strong>Start Video Stream and Get Description:</strong></p>
        <ul>
            <li>Press the "Select Camera" button to start the video stream.</li>
            <li>Press the "Describe the frame" button to get the description of the video frame.</li>
            <li>Press the "Text-to-Speech" button to hear the description audibly.</li>
        </ul>
    </li>
</ol>

<h2>Example</h2>
<p>To see an example of the application in action, refer to the following steps:</p>
<ol>
    <li>Select Camera: Choose the desired camera source from the dropdown menu.</li>
    <li>Select Language: Choose the language for the description from the language menu.</li>
    <li>Start Video Stream: Click "Select Camera" to start the video stream.</li>
    <li>Describe Frame: Click "Describe the frame" to get a textual description of the current video frame.</li>
    <li>Text-to-Speech: Click "Text-to-Speech" to hear the description spoken aloud.</li>
</ol>


</body>
</html>

<body>
  <h1>🐍 Snake Game with Tkinter 🎮</h1>
  <p>A simple Snake game implemented in Python using the Tkinter library. The snake moves automatically toward food placed by mouse clicks. The snake grows by eating food and shrinks gradually if it exceeds a certain length.</p>

  <h2>✨ Features</h2>
  <ul>
    <li>🐍 Classic snake movement with segments</li>
    <li>🎯 Automatic movement toward the nearest food</li>
    <li>🖱️ User can add food by clicking anywhere on the window</li>
    <li>🍎 Snake grows by eating food</li>
    <li>⏳ Snake shrinks automatically every minute if longer than the maximum allowed length</li>
    <li>↩️ Bouncing off window edges</li>
    <li>🎨 Visual feedback: snake head is black, body segments are red, food is brown</li>
  </ul>

  <h2>🛠️ Requirements</h2>
  <ul>
    <li>🐍 Python 3.x</li>
    <li>📦 Tkinter (usually included with Python installations)</li>
  </ul>

  <h2>🚀 How to Run</h2>
  <ol>
    <li>Clone or download this repository.</li>
    <li>Run the <code>snake.py</code> script:</li>
  </ol>
  <pre><code>python snake.py</code></pre>
  <ol start="3">
    <li>The game window opens in fullscreen mode.</li>
    <li>Click anywhere in the window to add food.</li>
    <li>The snake will automatically move toward and eat the food.</li>
    <li>To exit fullscreen, press <code>Esc</code> or close the window.</li>
  </ol>

  <h2>🎮 Controls</h2>
  <ul>
    <li>🖱️ <strong>Left mouse click</strong>: Place food on the game board.</li>
  </ul>

  <h2>🧩 How It Works</h2>
  <ul>
    <li>🐍 The snake starts at the center of the window.</li>
    <li>🔄 The snake moves in steps, automatically changing direction toward the closest food.</li>
    <li>🍎 When the snake eats food, it grows by adding a segment.</li>
    <li>🔻 If the snake length exceeds a predefined maximum, it will shrink gradually over time, removing the last segments with a blinking effect.</li>
    <li>↩️ The snake bounces off the edges of the window instead of disappearing.</li>
  </ul>

  <h2>⚙️ Customization</h2>
  <ul>
    <li>⏩ Change <code>step</code> to adjust the speed and step size of the snake.</li>
    <li>🔘 Change <code>segment_radius</code> to modify the size of snake segments and food.</li>
    <li>📏 Adjust <code>max_size</code> to set the maximum snake length before shrinking.</li>
    <li>⏲️ Modify <code>shrink_time</code> to control how often the snake shrinks (in milliseconds).</li>
  </ul>

  <h2>📄 License</h2>
  <p>This project is open-source and free to use.</p>
</body>

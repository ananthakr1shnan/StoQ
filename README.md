# Stoq

## Inspiration
Investing can be overwhelming for beginners and non-technical individuals who understand the market but lack the skills to code or analyze data effectively. We envisioned a platform that empowers these users by simplifying the complexities of the stock market while making algorithmic trading more accessible. Leveraging lightning-fast AI technology, our goal is to create a seamless experience for anyone to explore, learn, and implement investment strategies in real-time.

## What it Does
Stoq is a powerful financial insights platform designed to cater to:

- **Beginners:** Users new to the stock market can learn investing principles through engaging, interactive conversations.
- **Non-technical Investors:** Those with market knowledge but no coding skills can create, test, and refine trading strategies effortlessly.

### Key Features
- **Simplified Education:** Breaks down complex market concepts into easy-to-understand explanations, making it beginner-friendly.
- **Natural Language Strategy Building:** Allows users to describe trading ideas in plain language, translating these into functional strategies.
- **Real-Time Testing:** Tests strategies in a simulated environment with realistic market data.
- **Actionable Feedback:** Provides clear, helpful recommendations to refine and improve strategies.
- **Graph Integration with Vision Models:** Generates performance graphs and seamlessly integrates them into Llama 90B Vision, enhancing visual analysis with cutting-edge image modeling.

## How We Built It
We used a combination of cutting-edge technologies to bring Stoq to life:

- **SambaNova Cloud:** Enabled high-speed data processing and real-time AI responses, ensuring an efficient and responsive user experience. Integrated Llama 90B Vision for graph visualization and Llama 3.1 8B for chatbot functionality.
- **Autogen:** Powered autonomous agents guiding users through strategy creation, testing, and refinement.
- **Cohere:** Used for embedding functions, translating natural language inputs into actionable insights.
- **Groq:** Enhanced educational tools and strategy testing environments with data-driven contextual insights.
- **Next.js:** Built a clean, intuitive frontend with drag-and-drop tools and interactive prompts.
- **Flask:** Supported backend operations, including user input processing, algorithm testing, and real-time feedback delivery.

## Challenges We Ran Into
- Translating natural language trading ideas into precise algorithms without overwhelming users with technical jargon.
- Balancing educational content for beginners with the functional needs of experienced investors.
- Delivering actionable, easy-to-understand feedback while maintaining realistic simulations based on market data.
- Integrating graph data seamlessly with vision models for advanced visual insights.

## Accomplishments That We're Proud Of
- Building a platform that empowers non-technical users to create, test, and refine trading strategies without needing to write code.
- Successfully integrating graph outputs into Llama 90B Vision for state-of-the-art data visualization.
- Leveraging high-speed AI technology to deliver real-time insights and feedback for strategy testing.
- Simplifying financial education by combining interactivity with actionable recommendations.
- Developing a scalable, beginner-friendly solution that bridges the gap between financial knowledge and algorithmic trading.

## What We Learned
- Designing for non-technical users requires deep empathy and a focus on simplicity without sacrificing functionality.
- Real-time AI capabilities can transform how users interact with complex systems like financial markets.
- Leveraging advanced vision models such as Llama 90B Vision opens new possibilities for visual data representation.
- Iterative testing with diverse users was essential for refining the platform to meet the needs of both beginners and experienced investors.

## What’s Next for Stoq
- **Community Sharing:** Enable users to share and explore trading strategies created by others.
- **Predictive Analytics:** Add advanced AI capabilities to provide market performance predictions for user strategies.
- **Live Trading Integration:** Allow users to connect their strategies to real-world trading platforms securely and efficiently.
- **Custom AI Models:** Tailor the platform to specific industries or trading styles based on user feedback.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/stoq.git
   cd stoq
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. Set up environment variables in a `.env` file:
   ```env
   SAMBANOVA_API_KEY=your_api_key
   COHERE_API_KEY=your_api_key
   FLASK_ENV=development
   ```

4. Run the backend server:
   ```bash
   flask run
   ```

5. Run the frontend:
   ```bash
   npm run dev
   ```

6. Access the platform at `http://localhost:3000`.

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- **SambaNova Cloud:** For their high-speed AI and vision model capabilities.
- **Cohere:** For embedding functions.
- **Autogen:** For autonomous agent frameworks.
- **Perplexity:** For data-driven contextual insights.


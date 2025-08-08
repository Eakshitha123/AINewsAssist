document.getElementById("keywordForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const keyword = document.getElementById("keywordInput").value;
  getNews(keyword);
});

function getNews(keyword) {
  // This is placeholder. We'll add real API logic next.
  const dummyData = [
    {
      title: "OpenAI wins $200M Defense Contract",
      description: "OpenAI to provide AI tools for proactive cyber defense.",
      url: "https://www.theverge.com/openai-contract"
    }
  ];

  displayResults(dummyData);
}

function displayResults(articles) {
  const container = document.getElementById("newsResults");
  container.innerHTML = "";

  articles.forEach(article => {
    const div = document.createElement("div");
    div.innerHTML = `
      <h3>${article.title}</h3>
      <p>${article.description}</p>
      <a href="${article.url}" target="_blank">Read more</a>
      <hr />
    `;
    container.appendChild(div);
  });
}

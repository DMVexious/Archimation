document.addEventListener('DOMContentLoaded', () => {

  const topicForm = document.getElementById('topic-form');

  if (topicForm) {
    
    topicForm.addEventListener('submit', (event) => {
      event.preventDefault();

      const topicInput = document.getElementById('topic-input');
      const topicValue = topicInput.value.trim(); // .trim() removes whitespace

      if (topicValue) {
        console.log('Topic saved:', topicValue);
        alert(`You've chosen the topic: ${topicValue}`);
        
        topicInput.value = '';

      } else {
        alert('Please enter a topic before starting the journey!');
      }
    });
  }
});
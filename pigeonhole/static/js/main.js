// // Add event listeners to the select inputs
// const topicSelect = document.getElementById('topic-select');
// const issueSelect = document.getElementById('issue-select');

// topicSelect.addEventListener('change', filterProjects);
// issueSelect.addEventListener('change', filterProjects);

// // Create a function to filter projects based on selected topics and issues
// function filterProjects() {
//     console.log('filtering projects');
//     const searchQuery = document.getElementById('search-input').value;
//     let selectedTopics = Array.from(topicSelect.selectedOptions).map(option => option.value);
//     let selectedIssues = Array.from(issueSelect.selectedOptions).map(option => option.value);

//     // Update the lists of selected topics and issues
//     updateSelectedList(topicSelect, 'selected-topics-list');
//     updateSelectedList(issueSelect, 'selected-issues-list');

//     // Check if selectedTopics and selectedIssues are empty, and set them to null if necessary
//     selectedTopics = selectedTopics.length === 0 ? null : selectedTopics;
//     selectedIssues = selectedIssues.length === 0 ? null : selectedIssues;

//     renderProjectCards(searchQuery, selectedTopics, selectedIssues);
// }

// function updateSelectedList(selectElement, listElementId) {
//     const listElement = document.getElementById(listElementId);
//     listElement.innerHTML = ''; // Clear the existing list items

//     // Add new list items for each selected option
//     Array.from(selectElement.selectedOptions).forEach(option => {
//         const listItem = document.createElement('li');
//         listItem.textContent = option.text;
//         listElement.appendChild(listItem);
//     });
// }

// // Add an event listener to the 'load' event to populate the select inputs
// window.addEventListener('load', () => {
//     fetch('api/static_data/projects.json')
//         .then((response) => response.json())
//         .then((data) => {
//             const uniqueTopics = new Set();
//             const uniqueIssues = new Set();

//             // Collect unique topics and issues
//             for (const [key, value] of Object.entries(data)) {
//                 for (const topic of value.gh_topics) {
//                     uniqueTopics.add(topic);
//                 }

//                 for (const issueType of Object.keys(value.gh_issues_dict)) {
//                     uniqueIssues.add(issueType);
//                 }
//             }

//             // Populate the topic select input
//             for (const topic of uniqueTopics) {
//                 const option = document.createElement('option');
//                 option.value = topic;
//                 option.textContent = topic;
//                 topicSelect.appendChild(option);
//             }

//             // Populate the issue select input
//             for (const issueType of uniqueIssues) {
//                 const option = document.createElement('option');
//                 option.value = issueType;
//                 option.textContent = issueType;
//                 issueSelect.appendChild(option);
//             }

//             updateSelectedList(topicSelect, 'selected-topics-list');
//             updateSelectedList(issueSelect, 'selected-issues-list');
//         });
// });
// // main.js
// document.addEventListener('DOMContentLoaded', (event) => {
//     const clearButtons = document.querySelectorAll('.clear-button');

//     clearButtons.forEach(button => {
//         button.addEventListener('click', clearSelected);
//     });
// });

// function clearSelected(event) {
//     // Identify which button was clicked
//     const buttonId = event.target.id;

//     // Determine which list to clear based on the button ID
//     let listToClear;
//     if (buttonId === 'clear-topics') {
//         listToClear = document.getElementById('selected-topics-list');
//     } else if (buttonId === 'clear-issues') {
//         listToClear = document.getElementById('selected-issues-list');
//     }

//     // Clear the identified list
//     if (listToClear) {
//         listToClear.innerHTML = ''; // This removes all child elements in the list
//     }

//     console.log('clearing selected:', buttonId)
//     // If you also need to clear the selections from the <select> elements
//     if (buttonId === 'clear-topics') {
//         const topicSelect = document.getElementById('topic-select');
//         Array.from(topicSelect.options).forEach(option => option.selected = false);
//         const selectedTopics = document.getElementById('selected-topics-list');
//         //  Remove all list items from the selected topics list
//         selectedTopics.innerHTML = '';

//     } else if (buttonId === 'clear-issues') {
//         const issueSelect = document.getElementById('issue-select');
//         Array.from(issueSelect.options).forEach(option => option.selected = false);
//         const selectedIssues = document.getElementById('selected-issues-list');
//         //  Remove all list items from the selected issues list
//         selectedIssues.innerHTML = '';
//     }

//     // You may need to call some function to update other parts of the UI or state
//     // For example, re-render the project cards if they depend on these filters
//     const searchQuery = document.getElementById('search-input').value;
//     let selectedTopics = Array.from(topicSelect.selectedOptions).map(option => option.value);
//     let selectedIssues = Array.from(issueSelect.selectedOptions).map(option => option.value);
//     renderProjectCards(searchQuery, selectedTopics, selectedIssues);
// }

// function removeItem(event, itemValue) {
//     // Handle removing the specific item both visually and logically
//     event.target.parentNode.remove();
//     // Further logic to unselect the item from the actual select element goes here
//     const listItem = document.createElement('li');
//     listItem.textContent = selectedValue;
//     const removeButton = document.createElement('button');
//     removeButton.classList.add('remove-item-button');
//     removeButton.onclick = (event) => removeItem(event, selectedValue);
//     listItem.appendChild(removeButton);
//     document.getElementById('selected-topics-list').appendChild(listItem);
// }

// // Add event listeners for search inputs
// document.getElementById('topic-search').addEventListener('input', handleTopicSearch);
// document.getElementById('issue-search').addEventListener('input', handleIssueSearch);

// function handleTopicSearch() {
//     const searchTerm = this.value.toLowerCase();
//     // const topicSelect = document.getElementById('topic-select');

//     Array.from(topicSelect.options).forEach((option) => {
//         const text = option.textContent.toLowerCase();
//         option.selected = text.includes(searchTerm);
//     });

// }

// function handleIssueSearch() {
//     const searchTerm = this.value.toLowerCase();
//     // const issueSelect = document.getElementById('issue-select');

//     Array.from(issueSelect.options).forEach((option) => {
//         const text = option.textContent.toLowerCase();
//         option.selected = text.includes(searchTerm);
//     });

// }
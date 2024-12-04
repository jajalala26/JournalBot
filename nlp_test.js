const { NlpManager } = require('node-nlp');
const manager = new NlpManager({ languages: ['en'] });

manager.addDocument('en', 'I feel great!', 'emotions.positive');
manager.addDocument('en', 'I am so happy right now!', 'emotions.positive');
manager.addDocument('en', 'This is amazing!', 'emotions.positive');
manager.addDocument('en', 'I’m excited!', 'emotions.positive');
manager.addDocument('en', 'I’m so glad!', 'emotions.positive');

manager.addDocument('en', 'I feel terrible...', 'emotions.negative');
manager.addDocument('en', 'I’m feeling down.', 'emotions.negative');
manager.addDocument('en', 'This is so frustrating.', 'emotions.negative');
manager.addDocument('en', 'I’m so angry!', 'emotions.negative');
manager.addDocument('en', 'I’m really upset.', 'emotions.negative');

manager.addAnswer('en', 'emotions.positive', 'I’m so glad to hear that! Keep up the positive energy!');
manager.addAnswer('en', 'emotions.positive', 'That’s awesome! Keep smiling!');
manager.addAnswer('en', 'emotions.positive', 'Yay! It’s great to hear that you’re feeling good!');
manager.addAnswer('en', 'emotions.negative', 'I’m sorry you feel that way. I’m here if you want to talk.');
manager.addAnswer('en', 'emotions.negative', 'It’s okay to feel down sometimes. Take care of yourself.');
manager.addAnswer('en', 'emotions.negative', 'I understand. I hope things get better soon!');

manager.addDocument('en', 'goodbye for now', 'greetings.bye');
manager.addDocument('en', 'bye bye take care', 'greetings.bye');
manager.addAnswer('en', 'greetings.bye', 'Till next time');
manager.addAnswer('en', 'greetings.bye', 'See you soon!');

(async () => {
    await manager.train();
    manager.save();
    
    let response = await manager.process('en', 'I feel great!');
    console.log('Positive Test: ', response);

    response = await manager.process('en', 'I feel terrible...');
    console.log('Negative Test: ', response);

    response = await manager.process('en', 'I should go now');
    console.log('Goodbye Test: ', response);
})();

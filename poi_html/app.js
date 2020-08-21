const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const { conn } = require('./config');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('/driving', (req, res) => {
    res.sendFile(__dirname + '/driving.html');
});

app.post('/api', (req, res) => {
    const {pois, hash} = req.body;
    const rows = pois.map(poi => {
        return {
            ...poi,
            hashcode: hash
        }
    })
    conn.batchInsert('poi_profile', rows)
        .then(() => console.log('inserted'))
        .catch(err => console.log(err));
    res.send('ok'); // 必须
});

app.listen(7000, () => {
    console.log('poi-salve app listenting on port 7000!');
})
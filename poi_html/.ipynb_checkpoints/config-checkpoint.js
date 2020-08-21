const mysql = {
    client: 'mysql',
    connection: {
        host: '127.0.0.1',
        port: '3306',
        user: 'root',
        password: 'Hyk221522.',
        database: 'poi',
    }
};

const conn = require('knex')(mysql);

module.exports = { conn };

const tianjing = '和平区|河东区|河西区|南开区|河北区|红桥区|东丽区|西青区|津南区|北辰区|武清区|宝坻区|滨海新区|宁河区|静海区';
const wuhan = '江岸区|江汉区|硚口区|汉阳区|武昌区|青山区|洪山区|东西湖区|汉南区|蔡甸区|江夏区|黄陂区|新洲区'
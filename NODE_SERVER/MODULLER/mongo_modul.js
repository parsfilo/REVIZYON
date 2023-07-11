var { exec } = require("child_process");

var MongoClient = require('mongodb').MongoClient;

const DB_NAME = "CIHAZ_VERILER";
const SISMIK_COL_NAME = "SON_SISMIK";
const DEPREM_COL_NAME = "SON_DEPREM";
const LOCAL_MONGO_URL = 'mongodb://0.0.0.0:27017';
const client = new MongoClient(LOCAL_MONGO_URL);


module.exports = {

    MONGO_KAYIT_SORGULA: async function (io, remote_server_soket_client) {
        await client.connect();
        const db = client.db(DB_NAME);
        const SISMIK_COL = db.collection(SISMIK_COL_NAME);
        const SISMIK_COL_query = { SISMIK_ALARM_ZAMANI: { $gt: 1 } };
        const SISMIK_COL_options = { sort: { _id: -1 }, projection: { _id: 0, SISMIK_ALARM_ZAMANI: 1, x_std: 1, y_std: 1, z_std: 1, mmi_olcek: 1 } };
        const SISMIK_COL_findResult = await SISMIK_COL.find(SISMIK_COL_query, SISMIK_COL_options).limit(3).toArray();

        const DEPREM_COL = db.collection(DEPREM_COL_NAME);
        const DEPREM_COL_query = { DEPREM_ALARM_ZAMANI: { $gt: 1 } };
        const DEPREM_COL_options = { sort: { _id: -1 }, projection: { _id: 0, DEPREM_ALARM_ZAMANI: 1, x_std: 1, y_std: 1, z_std: 1, mmi_olcek: 1 } };
        const DEPREM_COL_findResult = await DEPREM_COL.find(DEPREM_COL_query, DEPREM_COL_options).limit(3).toArray();

        io.emit('son_sismik', SISMIK_COL_findResult);
        io.emit('son_deprem', DEPREM_COL_findResult);
        remote_server_soket_client.emit('sismik_aktivite_dict', SISMIK_COL_findResult);
        remote_server_soket_client.emit('deprem_aktivite_dict', DEPREM_COL_findResult);
        client.close()

    },

    VERITABANI_SIFIRLA_FONK: async function () {
        var SISMIK_VERI = [
            { SISMIK_ALARM_ZAMANI: 1640984400, x_std: 0, y_std: 0, z_std: 0, r_std: 0, mmi_olcek: 0 },
            { SISMIK_ALARM_ZAMANI: 1640984400, x_std: 0, y_std: 0, z_std: 0, r_std: 0, mmi_olcek: 0 },
            { SISMIK_ALARM_ZAMANI: 1640984400, x_std: 0, y_std: 0, z_std: 0, r_std: 0, mmi_olcek: 0 }
        ];
        var DEPREM_VERI = [
            { DEPREM_ALARM_ZAMANI: 1640984400, x_std: 0, y_std: 0, z_std: 0, r_std: 0, mmi_olcek: 0 },
            { DEPREM_ALARM_ZAMANI: 1640984400, x_std: 0, y_std: 0, z_std: 0, r_std: 0, mmi_olcek: 0 },
            { DEPREM_ALARM_ZAMANI: 1640984400, x_std: 0, y_std: 0, z_std: 0, r_std: 0, mmi_olcek: 0 }
        ];
        await client.connect();
        const db = client.db(DB_NAME);
        const SISMIK_COL = db.collection(SISMIK_COL_NAME);
        const DEPREM_COL = db.collection(DEPREM_COL_NAME);
        const SISMIK_COL_deleteResult = await SISMIK_COL.deleteMany({ SISMIK_ALARM_ZAMANI: { $gt: 1 } });
        const DEPREM_COL_deleteResult = await DEPREM_COL.deleteMany({ DEPREM_ALARM_ZAMANI: { $gt: 1 } });
        const SISMIK_COL_insertResult = await SISMIK_COL.insertMany(SISMIK_VERI);
        const DEPREM_COL_insertResult = await DEPREM_COL.insertMany(DEPREM_VERI);
        exec('rm -rf /home/pi/Desktop/REVIZYON/EKRAN_GORUNTULERI');
        client.close()
        return 'VERITABANI_SIFIRLANDI !';
    }
}
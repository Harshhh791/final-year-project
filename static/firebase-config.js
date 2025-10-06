// firebase-config.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/9.6.10/firebase-auth.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-database.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyC6lScAoL0j9HYlWkj8V7BldIqBTVZXRoI",
    authDomain: "scholarship-prediction.firebaseapp.com",
    databaseURL: "https://scholarship-prediction-default-rtdb.firebaseio.com",
    projectId: "scholarship-prediction",
    storageBucket: "scholarship-prediction.appspot.com",
    messagingSenderId: "471946287433",
    appId: "1:471946287433:web:7564029f16d316d8c4e298",
    measurementId: "G-H5R07M4ZLV"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const database = getDatabase(app);

export { auth, database, createUserWithEmailAndPassword, signInWithEmailAndPassword, ref, set };

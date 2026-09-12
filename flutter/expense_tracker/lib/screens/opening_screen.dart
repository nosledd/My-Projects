/*

import 'package:flutter/material.dart';
import 'home_screen.dart';

class OpeningScreen extends StatelessWidget {
  const OpeningScreen({super.key});

  @override
  Widget build(BuildContext context) {
    Future.delayed(Duration(seconds: 0), () {
      Navigator.pushReplacement(context,                        // replaces and deletes the current widget
        MaterialPageRoute(builder: (BuildContext context) {     // routes to login screen
          return LoginScreen();
        },
        ),
      );
    });

    return Scaffold(
      body: Center(
        child: Text(
            "Nosled",
            style: TextStyle(
              fontFamily: "Joseph",
              fontSize: 30,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.5,
              color: Colors.black,
            )
        ),

      ),
    );
  }
}

*/
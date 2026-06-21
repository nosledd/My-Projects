import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'package:google_fonts/google_fonts.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: true,

    //  Color(0XFF1D4ED8),

      theme: ThemeData(
        splashFactory: NoSplash.splashFactory, // This removes the wierd splash ripple everywhere
        textTheme: GoogleFonts.poppinsTextTheme(),
      ),




      home: const HomeScreen(),
    );
  }
}

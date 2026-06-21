import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'home.dart';
import 'add.dart';
import 'history.dart';


class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

  int _selectedIndex = 0;

  void _navigationBar(int index){

    if (index == 3) {
      /*   Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => PdfView()),
      ); */
    }



    else {
      setState(() {
       _selectedIndex = index;
      });
    }
  }

  final List<Widget> _pages = [
    Home(),
    AddExpense(),
    historyScreen(),
    Home(),
  ];

  @override
  Widget build(BuildContext context) {
    final ScreenWidth = MediaQuery.of(context).size.width;
    final ScreenHeight = MediaQuery.of(context).size.height;
    return PopScope(     // Used to Control Back button behavior
      canPop: false,     // if True then i can go back using back button + Arrow Button
      child: Scaffold(
        body: _pages[_selectedIndex],     // Tells the List which Index
        bottomNavigationBar:  Theme(     // Added because buttons behave weirdly when taped
          data: Theme.of(context).copyWith(
            splashColor: Colors.transparent,
            highlightColor: Colors.transparent,
          ),
          child:  Container(
            decoration: BoxDecoration(
              border: Border(
                top: BorderSide(color: Colors.white10),
              ),
            ),
            child:
            BottomNavigationBar(          // We can use NavigationBar. its the latest widget
                type: BottomNavigationBarType.fixed,  // Fies the bug which cause when they are 3+ buttons
                // backgroundColor: Color(0xFF141218),
                unselectedItemColor: Colors.black54,
                selectedItemColor: Color(0XFF1D4ED8),
                unselectedLabelStyle: GoogleFonts.poppins(fontWeight: FontWeight.bold),
                selectedLabelStyle: GoogleFonts.poppins(fontWeight: FontWeight.bold),
                currentIndex: _selectedIndex,
                onTap: _navigationBar,
                items: [
                  BottomNavigationBarItem(icon: Icon(Icons.home_rounded), label: "Home"),
                  BottomNavigationBarItem(icon: Icon(Icons.add_circle_rounded), label: "Add"),
                  BottomNavigationBarItem(icon: Icon(Icons.history_rounded), label: "History"),
                  BottomNavigationBarItem(icon: Icon(Icons.bar_chart_rounded), label: "Insights"),
                ]),
          ),
        ),




      ),
    );
  }
}














    /*
@override
  Widget build(BuildContext context) {
    return Scaffold(
        body:  Stack(
        children: [

          // Background
          Container(
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: AssetImage("assets/black_ui.jpg"),     // Custom Image
                fit: BoxFit.cover,
              ),
            ),
          ),




           Align(
             alignment: Alignment(0, -0.70),

              child:DefaultTextStyle(
                style: TextStyle(
                  fontFamily: "Joseph",     // Custom Font
                  fontWeight: FontWeight.w700,
                  fontSize: 30,
                 ),

              child:Column(                                       // Refer Page 12
                mainAxisSize: MainAxisSize.min,       // Column wise text space, without it the align will also calculate the empty space, main is column wise because we are use widget column
                crossAxisAlignment: CrossAxisAlignment.center,   // This is the reason why the text in properly centered with each other, it takes width of the words and centers them
                children: [
                  Text("LOGIN TO"),
                  Text("YOUR ACCOUNT"),

                ],
              ),
              ),
             ),




          Positioned(           /*First you position it then let the left and right free,
                                   Then use Align property to easily align without the pixels*/
            bottom: -10,
            left: 0,
            right: 0,

            child: Align(
              alignment: Alignment.bottomCenter,

            child: SizedBox(        // can use container too
              width: 375,
              height: 525,

            child: ClipRRect(             // it is needed already cross checked
              borderRadius: BorderRadius.circular(12),

              child: BackdropFilter(           // it is needed already cross checked
                filter: ImageFilter.blur(
                  sigmaX: 10,
                  sigmaY: 15,
                ),

                child: Container(
                  height: 300,
                  width: 250,


                   padding: EdgeInsets.all(20),
                   decoration: BoxDecoration(
                     color: Colors.white.withValues(alpha: 0.10),
                   border: Border.all(
                     color: Colors.white.withValues(alpha: 0.10),


                    ),
                         borderRadius: BorderRadius.circular(12),
                     ),



                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [


                          Text(
                            "Enter your login information",
                            style: TextStyle(
                              fontFamily: "Joseph",
                              fontWeight: FontWeight.w300,
                              fontSize: 19,
                            ),
                          ),

                          SizedBox(height: 16),

                          TextField(
                            keyboardType: TextInputType.emailAddress,

                            decoration: InputDecoration(
                              hintText: "Email",

                              prefixIcon: Icon(Icons.alternate_email_outlined),

                              border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(20),
                              ),
                            ),
                          ),

                          SizedBox(height: 20),

                          TextField(                        //need to be changed
                            obscureText: true,

                            decoration: InputDecoration(
                                hintText: "Password",

                                prefixIcon: Icon(Icons.lock_outline),

                                suffixIcon: Icon(Icons.visibility), // optional eye toggle

                                border: OutlineInputBorder(
                                  borderRadius: BorderRadius.circular(20),
                              )
                            ),
                          ),

                          SizedBox(height: 20),

                          ElevatedButton.icon(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.blue, // Button background color
                              foregroundColor: Colors.white,
                              fixedSize: const Size(500, 50),

                            ),
                          onPressed: () {},           // need to be changed 

                          label: Text("LOGIN"),
                         ),
                       ],
                      ),



                    ),

               ),

            ),
          ),

            ),

          ),


        ],
      ),
    );
  }
}


     */
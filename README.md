# Thesis-Text-based-Video-Game
A text based video game that demonstrates procedural narrative and dynamic dialogues.

Εγκατάσταση του παιχνιδιού:
1. Κατεβάστε το συμπιεσμένο αρχείο που περιέχει όλους τους φακέλους και τα αρχεία κώδικα από αυτό το αποθετήριο
2. Αποσυμπιέστε τα περιεχόμενα σε φάκελο της επιλογής σας
3. Με Python, τρέξτε το αρχείο setup.py ώστε να εγκατασταθούν οι απαραίτητες βιβλιοθήκες που χρειάζονται για να λειτουργήσει το παιχνίδι
4. Τρέξτε το αρχείο main.py, αυτό είναι το παιχνίδι

Σε περίπτωση σφάλματος Errno [13 Permission denied] τρέξτε το εργαλείο ανάπτυξης κώδικα που χρησιμοποιείτε με δικαιώματα διαχειριστή, αν δεν το κάνετε ήδη.

Για το πώς να παίξετε το παιχνίδι ακολουθούν οδηγίες, οι οποίες υπάρχουν και εντός του περιβάλλοντος του παιχνιδιού στα Tutorials.

Μετακίνηση στον κόσμο του παιχνιδιού:
Ο χάρτης του παιχνιδιού έχει παραχθεί διαδικαστικά, αποτελείται από έναν πίνακα 50x50 δωματίων - σκηνών του παιχνιδιού, όπου κάθε δωμάτιο απεικονίζεται ως τετράγωνο, με το χρώμα να δείχνει τι τύπου δωματίου είναι (πράσινο για πεδιάδα, σκούρο καφέ για βουνό, μπλε για θάλασσα, άσπρο για κατοικήσιμη περιοχή κλπ). Με το κόκκινο χρώμα υποδεικνύεται η τρέχουσα θέση του παίχτη, με μαύρο χρώμα απεικονίζεται η θέση κάποιου σημείου ενδιαφέροντος, όπως του στόχου σε κάποια αποστολή και το κίτρινο χρώμα δείχνει σε ποια σημεία ο παίχτης ανέλαβε μια αποστολή από κάποιον χαρακτήρα. Με τις εντολές go DIRECTION όπου DIRECTION είναι μία από τις (north, south, east, west, nothwest, northeast, southwest, southeast) ο παίχτης μπορεί να μετακινηθεί από το δωμάτιο που βρίσκεται σε γειτονικό δωμάτιο. Μπορεί επίσης να μετακινηθεί κάνοντας κλικ σε κάποιο δωμάτιο στον χάρτη, αρκεί να μην απέχει πάνω από πέντε δωμάτια απόσταση από το τωρινό δωμάτιο στο οποίο βρίσκεται.

Συνομιλία με χαρακτήρες:
Ο παίχτης στο ταξίδι του θα συναντήσει διάφορους χαρακτήρες, από τους οποίους μπορεί να ζητήσει κάποια αποστολή, να αγοράσει πράγματα, ή να ρωτήσει διάφορες πληροφορίες. Ο παίχτης μπορεί να ρωτήσει τα ονόματα των χαρακτήρων που συναντάει, με κάποια από τις εντολές name/what is your name? Για να συνομιλήσει με χαρακτήρα, πρέπει να πληκτρολογήσει την εντολή talk to CHARACTER, όπου CHARACTER είτε το όνομα του χαρακτήρα (το μικρό του όνομα, ή το ονοματεπώνυμο), είτε την ιδιότητά του (το επάγγελμα του, όπως merchant, blacksmith, sorcerer, captain κλπ). Με την εντολή αυτή, θα ανοίξει ένα μενού επιλογών διαλόγου, στο οποίο ο παίχτης μπορεί να συνομιλήσει με τον χαρακτήρα.

Αποστολές:
Σε συζητήσεις με άλλους χαρακτήρες, ο παίχτης μπορεί να ζητήσει να του αναθέσουν κάποια δουλειά, κάνοντας τις κατάλληλες επιλογές στο μενού διαλόγων. Αν δεχτεί τη δουλειά, τότε η αποστολή αυτή θα μπει στη λίστα των Quests και θα μπορεί από το αντίστοιχο μενού να δει πληροφορίες για αυτήν, όπως ποιος του ανέθεσε τη δουλειά, τι ψάχνει και πού βρίσκεται ο στόχος. Υπάρχουν διαφορετικού τύπου πιθανές αποστολές, όπως το κυνήγι επικηρυγμένων, η εύρεση χαμένων αντικειμένων, η διάσωση ατόμου κλπ, και για ανταμοιβή ο παίχτης μπορεί να κερδίσει είτε λεφτά είτε νέα αντικείμενα για να χρησιμοποιήσει στο ταξίδι του. Σχεδόν κάθε ένας από τους εκατοντάδες χαρακτήρες στο παιχνίδι έχουν από μία μοναδική αποστολή που μπορούν να δώσουν στον παίχτη.

Αγορές και πωλήσεις με άλλους χαρακτήρες:
Κάποιοι χαρακτήρες στο παιχνίδι είναι έμποροι, σιδηρουργοί ή ξενοδόχοι, οπότε έχουν αντικείμενα να πουλήσουν που μπορεί να είναι χρήσιμα για το ταξίδι του παίχτη. Με τις εντολές buy ITEM from CHARACTER και sell ITEM to CHARACTER, όπου ITEM το πλήρες όνομα του αντικειμένου και CHARACTER με τον ίδιο τρόπου που περιγράφεται παραπάνω, ο παίχτης μπορεί να αγοράσει αντικείμενο από τον χαρακτήρα για κάποιο ποσό, αλλά και να πουλήσει κάποιο δικό του. Επίσης μπορεί να δώσει κάποιο αντικείμενο χωρίς να ζητήσει αντίτιμο με τις εντολές give ITEM to CHARACTER/ return ITEM to CHARACTER.

Αντικείμενα:
Με την εντολή inventory ο παίχτης μπορεί να δει τι αντικείμενα έχει στο αποθετήριό του, τις περιγραφές τους, και τα λεφτά που έχει. Αν το αντικείμενο είναι όπλο, για να το κρατήσει στα χέρια του, αρκεί η εντολή equip ITEM. Για να αλλάξει πανοπλία ή ρούχο, η εντολή είναι wear ITEM. Τα αντικείμενα που καταναλώνονται, όπως φαγητά ή ποτά, χρησιμοποιούνται με την εντολή eat ITEM/ consume ITEM/ drink ITEM.
Πολλές φορές μπορεί να συναντήσει κάποιο αντικείμενο στο δρόμο, για να το πάρει, θα πρέπει να πληκτρολογήσει κάποια από τις εντολές take ITEM/ pick up ITEM/ get ITEM/ collect ITEM/ grab ITEM

Τα όπλα έχουν διαφορετική αποτελεσματικότητα ανάλογα με το πόσο καινούρια είναι, καθώς και διαφορετικό βάρος, το ίδιο ισχύει και για τις πανοπλίες. Τα φαγώσιμα όταν καταναλωθούν θα ανεβάσουν το HP του παίχτη.

Σύστημα μάχης:
Για επίθεση σε κάποιον χαρακτήρα, ο παίχτης πρέπει να πληκτρολογήσει την εντολή attack CHARACTER/ kill CHARACTER/ fight CHARACTER. Ο χαρακτήρας θα ανταποδώσει με δική του επίθεση και η μάχη συνεχίζεται μέχρι να μηδενιστούν τα HP κάποιου από τους δύο, ή ο παίχτης απλά 
φύγει από τη σκηνή-δωμάτιο. Σε αυτή την περίπτωση, το όπλο του παίχτη που χρησιμοποιείται, είναι αυτό που έχει εξοπλίσει με την εντολή equip ITEM, όπως και η πανοπλία είναι αυτή που έχει φορέσει με το wear ITEM. Επίσης, ο παίχτης μπορεί να χρησιμοποιήσει τη βαλίστρα που έχει διαθέσιμη με την εντολή shoot CHARACTER, καθώς και μπορεί να μάθει ξόρκια και να τα εξαπολύσει στους αντιπάλους του με την εντολή cast SPELL. Γράφοντας σκέτο spells εμφανίζονται τα διαθέσιμα ξόρκια που έχει ο παίχτης.

Κλοπή από άλλους χαρακτήρες:
Ο παίχτης μπορεί να κλέψει πράγματα από άλλους χαρακτήρες υπό προϋποθέσεις. Χρειάζεται το συνολικό βάρος αυτών που κουβαλάει (του όπλου που κρατάει αυτή τη στιγμή και της πανοπλίας που φοράει) να είναι χαμηλό ώστε να μην ακουστεί όταν προσπαθήσει να κλέψει. Αν όντως είναι πολύ ελαφρύς, η κλοπή με την εντολή steal from CHARACTER/ steal CHARACTER/ rob CHARACTER θα είναι πετυχημένη και ο χαρακτήρας δεν θα καταλάβει τον παίχτη. Αλλιώς, ο χαρακτήρας θα τον ακούσει και θα εκνευριστεί, μπορεί να  προσπαθήσει να επιτεθεί ο ίδιος στον παίχτη, ή να καλέσει φρουρούς άμα βρίσκονται σε πόλη, ή απλά να του ζητήσει τον λόγο. Με τον ίδιο τρόπο, ανάλογα με το βάρος του παίχτη μπορεί να προσπαθήσει να δολοφονήσει κρυφά κάποιον χαρακτήρα με την εντολή assassinate CHARACTER/ stealth kill CHARACTER.

Εγκλήματα:
Τα εγκλήματα που διαπράττει ο παίχτης τιμωρούνται στο παιχνίδι. Αν προσπαθήσει να κλέψει ή δολοφονήσει κάποιον και αποτύχει, τότε θα προκαλέσει την οργή του χαρακτήρα αυτού αλλά και θα αποκτήσει κακή φήμη προς άλλους χαρακτήρες. Αυτό σημαίνει οτί πολύ συχνά κάποιος θα προσπαθήσει να ζητήσει εκδίκηση από τον παίχτη, ή θα καλεί φρουρούς, ή απλώς θα αρνείται να βοηθήσει τον παίχτη. Σε περιπτώσεις που ο παίχτης σκοτώσει χαρακτήρα ενώ δεν βρίσκεται σε αυτοάμυνα (πχ. όταν κάποιος κλέφτης προσπαθήσει να επιτεθεί στον παίχτη), πάλι θα υπάρξουν παρόμοιες επιπτώσεις με αυτές που ήδη αναφέρθηκαν.

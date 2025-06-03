# Server-Client Text File Management System

- Server-ul gestionează o listă de fișiere text dintr-un director gazdă;
- Clientul se autentifică prin nume și primește lista fișierelor text, precum și numele utilizatorului care are în editare fiecare fișier;
- Orice client autentificat poate solicita spre vizualizare conținutul unui fișier, caz în care server-ul îi trimite ultima versiune de pe disc a acestuia;
- Un client poate solicita preluarea în editare a unui fișier disponibil, caz în care server-ul îi livrează conținutul acestuia și notifică ceilalți clienți că fișierul respectiv este în editare de către clientul care l-a solicitat;
- Clientul poate actualiza conținutul fișierului, solicitând server-ului salvarea noii versiuni, caz în care server-ul va actualiza pe disc conținutul fișierului cu ce a primit de la client și va notifica toți clienții care au în vizualizare acest fișier cu noul conținut, pentru a-și actualiza datele afișate;
- Clientul poate renunța la editarea fișierului, caz în care server-ul va notifica tuturor clienților autentificați că resursa respectivă nu mai este în editare de către clientul care o preluase, fiind disponibilă pentru preluarea în editare;
- La adăugarea sau ștergerea unui fișier de pe server, acesta va notifica toți clienții autentificați cu privire la numele fișierului afectat de operație, pentru a fi adăugat sau șters din lista fișierelor disponibile în client.

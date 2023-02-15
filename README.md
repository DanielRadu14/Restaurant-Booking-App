Tema2 SPRC
Radu Daniel 341C3


	Pentru realizarea temei, am folosit limbajul de programare python din considerente de simplitate a sintaxei si a familiaritatii cu acest limbaj, dar si pentru a putea folosi biblioteca Flask. Baza de date este realizata in MySQL deoarece este similara cu PL/SQL, singurul limbaj pe care il cunosc la momentul actual.

	Cele trei containere create si folosite sunt RestAPI-ul, baza de date MySQL si utilitarul MySQL Workbench folosit pentru gestionarea bazei de date. RestAPI-ul si baza de date se afla in intr-o retea, iar utilitarul si baza de date se afla in cea de-a doua retea, elementul comun intre cele trei fiind baza de date care se afla in ambele retele, din motive de modularitate, dar luand in calcul si dependentele dintre acestea.

	Userul cu care ma conectez la baza de date este root:daniel. Baza de date are definit un volum pentru persistenta datelor. Id-urile pentru inserarea in baza de date sunt generate automat printr-un contor global, individual pentru fiecare dintre cele trei tabele create.

	Userul se conecteaza la baza de date in fiecare ruta pentru a evita situatia cand serverul web porneste inaintea bazei de date iar utilizatorul nu se poate conecta. Pentru conectarea la baza de date, trebuie asteptat dupa finalizarea pornirii serverului MySQL.
	
	Pentru rularea aplicatiei este necesara doar rularea comenzii : docker-compose up --build

	Formatul de timestamp stocat in baza de date este: AAAA-LL-ZZ hh:mm:ss, dar comenzile care includ from_date si until_date de tipul GET /api/temperatures asteapta o data in format AAAA-LL-ZZ, cum a fost mentionat pe forum.

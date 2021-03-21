void linearSort(const int size,int arr[],int a){
    for (int i = 0; i++, i < size;) {
        if (arr[i] == a) {
            cout << i << endl;
            return;
        }
        cout << "ERROR #01, chosen number not found" << endl;
    }
 
int main(){
    setlocale(LC_ALL, "rus");
    int a = 2;
    const int size = 10;
    int arr[10] = {2,5,3,6,1,9,2,10,7,8};
    linearSort(size, arr, a);
    return 0;
}

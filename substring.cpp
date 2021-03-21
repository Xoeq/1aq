#include <cstdio>
#include <string>
#include <cstring>
 
void end(FILE* file, bool found, char* array) {
    fprintf(stdout, "%s", found ? "Yes" : "No");
    free(array);
    fclose(file);
}
bool compare(char* s, char* t, int id) {
    int k = 0;
    for (int i = id; i < strlen(t); i++) {
        if (s[i] != t[k++]) {
            return false;
        }
    }
    for (int i = 0; i < id; i++) {
        if (s[i] != t[k++]) {
            return false;
        }
    }
    return true;
}
int main(int argc, char** argv) {
    if (argc != 3) {
        fprintf(stderr, "Invalid program arguments. Two arguments required: <filename> <word>");
        return -1;
    }
    FILE* input = fopen(argv[1], "rb");
    if (input == nullptr) {
        fprintf(stderr, "File %s can not be opened", argv[1]);
        return -1;
    }
    if (strlen(argv[2]) == 0) {
        fprintf(stdout, "Yes");
        fclose(input);
        return 0;
    }
    char* t = static_cast<char *>(malloc(sizeof(argv[2])));
    int symbol;
    for (int i = 0; i < strlen(argv[2]); i++) {
        symbol = fgetc(input);
        if (symbol == EOF) {
            if (ferror(input)) {
                fprintf(stderr, "Error during reading");
                free(t);
                return -1;
            } else {
                end(input, false, t);
                return 0;
            }
        }
        t[i] = symbol;
    }
    if (compare(t, argv[2], 0)) {
        end(input, true, t);
        return 0;
    }
    if (symbol == EOF) {
        end(input, false, t);
        return 0;
    }
    int id = 0;
    while ((symbol = fgetc(input)) != EOF) {
        t[id++] = symbol;
        id %= strlen(t);
        if (compare(t, argv[2], id)) {
            end(input, true, t);
            return 0;
        }
    }
    if (ferror(input)) {
        fprintf(stderr, "Error during reading");
        free(t);
        return -1;
    }
    end(input, compare(t, argv[2], id), t);
    return 0;
}

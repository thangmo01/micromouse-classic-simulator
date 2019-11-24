#include <iostream>
#include <queue>

struct Position {
    short x;
    short y;
};

std::queue <Position> q;
short values[16][16];
short targets[4][2] = {{7,7}, {7,8}, {8,7}, {8,8}};

int main() {
    for (int i = 0; i < 16; i++) {
        for (int j = 0; j < 16; j++) {
            values[i][j] = -1;
        }
    }
    // push targets to queue
    for (int i = 0; i < 4; i++) {
        Position p;
        p.y = targets[i][0];
        p.x = targets[i][1];
        //set target
        values[p.y][p.x] = 0;
        q.push(p);
    }


    while (!q.empty()) {
        Position front = q.front();
        Position p;
        // North
        if (front.y - 1 >= 0 && values[front.y - 1][front.x] == -1) {
            p.y = front.y - 1;
            p.x = front.x;
            values[p.y][p.x] = values[front.y][front.x] + 1;
            q.push(p);
        }
        // East
        if (front.x + 1 < 16 && values[front.y][front.x + 1] == -1) {
            p.y = front.y;
            p.x = front.x + 1;
            values[p.y][p.x] = values[front.y][front.x] + 1;
            q.push(p);

        }
        // South
        if (front.y + 1 < 16 && values[front.y + 1][front.x] == -1) {
            p.y = front.y + 1;
            p.x = front.x;
            values[p.y][p.x] = values[front.y][front.x] + 1;
            q.push(p);
        }
        // West
        if (front.x - 1 >= 0 && values[front.y][front.x - 1] == -1) {
            p.y = front.y;
            p.x = front.x - 1;
            values[p.y][p.x] = values[front.y][front.x] + 1;
            q.push(p);
        }

        q.pop();
    }

    for (int i = 0; i < 16; i++) {
        std::cout << "[";
        for (int j = 0; j < 16; j++) {
            if (j < 16 - 1) {
                std::cout << values[i][j] << ",";
            }
            else {
                std::cout << values[i][j];
            }
        }
        std::cout << "],\n";
    }

    return 0;
}
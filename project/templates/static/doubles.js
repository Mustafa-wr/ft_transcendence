
var gameRunning = true;
var animationFrameID;
		localStorage.setItem('gamesFlag', 'true')
	startGame();
      async function startGame(){
      // Access the game field from the document
      const canvas = document.getElementById("game");
      // Make the field two-dimensional
      const context = canvas.getContext("2d");
      // Size of the game grid
      const grid = 15;
      // Height of the paddle
      const paddleHeight = grid * 5; // 80
      // Set the maximum distance the paddles can move downwards
      const TopLeftmaxPaddleY = canvas.height / 2 - paddleHeight ;
      const BottomLeftmaxPaddleY = canvas.height - grid - paddleHeight ;

      const TopRightmaxPaddleY = canvas.height / 2  - paddleHeight ; 
      const BottomRightmaxPaddleY = canvas.height - grid - paddleHeight ; 

      // // set the maximum distance the paddles can move upwards need to define for the lower paddles
      const BottomLeftminPaddleY = canvas.height / 2  ;
      const BottomRightminPaddleY = canvas.height / 2  ;

      // Paddle  and ball speed
      var paddleSpeed = 6;  
      var ballSpeed = 4;

      // Score
      var left_score = 0;
	  var right_score = 0;

      // Activate secret level
      var secret = false;
      // Number of bounces in secret mode
      var secret_count = 0;
      // Ball color, initially white
      ballColor = "white";
      
	  const paddleSpeedInput = document.getElementById('paddleSpeed');
		const ballSpeedInput = document.getElementById('ballSpeed');
	  
		// Apply customization options
		paddleSpeedInput.addEventListener('input', function () {
		  paddleSpeed = parseInt(paddleSpeedInput.value);
		});
	  
		ballSpeedInput.addEventListener('input', function () {
		  ballSpeed = parseInt(ballSpeedInput.value);
		});

		ballSpeedInput.addEventListener('input', function () {
			ballSpeed = parseInt(ballSpeedInput.value);
			ball.dx = (ball.dx > 0) ? ballSpeed : -ballSpeed;
			ball.dy = (ball.dy > 0) ? ballSpeed : -ballSpeed;
		  });

      
      // Describe the left paddles
      const topLeftPaddle = {
        // Place it in the center
        x: grid * 2,
        y: (canvas.height / 4 )- paddleHeight / 2,
        // Width - one grid cell
        width: grid,
        // Take the height from the constant
        height: paddleHeight,
        // The paddle doesn't move at the start
        dy: 0,
      };

      const bottomLeftPaddle = {
        x: grid * 2,
        y: (canvas.height * 3 / 4) - paddleHeight / 2,
        width: grid,
        height: paddleHeight,
        dy: 0,
      };


      // Describe the right paddles

      const topRightPaddle = {
        x: canvas.width - grid * 3,
        y: (canvas.height / 4) - paddleHeight / 2,
        width: grid,
        height: paddleHeight,
        dy: 0,
      };

      const bottomRightPaddle = {
        x: canvas.width - grid * 3,
        y: (canvas.height * 3 / 4) - paddleHeight / 2,
        width: grid,
        height: paddleHeight,
        dy: 0,
      };

      // Describe the ball
      const ball = {
        // It appears in the center of the field
        x: canvas.width / 2,
        y: canvas.height / 2,
        // Square, the size of a grid cell
        width: grid,
        height: grid,
        // At the start, the ball isn't scored, so remove the flag indicating that the ball needs to be reintroduced to the game
        resetting: false,
        // Serve the ball to the top right corner
        dx: ballSpeed,
        dy: -ballSpeed,
      };
      // Check whether two objects with known coordinates intersect or not
      // More details here: https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
      function collides(obj1, obj2) {
        return (
          obj1.x < obj2.x + obj2.width &&
          obj1.x + obj1.width > obj2.x &&
          obj1.y < obj2.y + obj2.height &&
          obj1.y + obj1.height > obj2.y
        );
      }

	//   function boundary_check(paddle, top, bottom) {
    //     if (paddle.y < top) {
    //       paddle.y = top;
    //     } else if (paddle.y > bottom) {
    //       paddle.y = bottom;
    //     }    
    //   }

      // Main game loop
      function loop() {
        // Clear the game field
		if (!gameRunning) {
			// Stop the game
			return;
		}
		context.clearRect(0, 0, canvas.width, canvas.height);
		if (left_score == 11 || right_score == 11){
			cancelAnimationFrame(animationFrameID);
			if (left_score == 11){
				alert("Game Over. Team left wins. !!");
			}
			else 
				alert("Game Over. Team right wins!!");
			localStorage.setItem('gamesFlag', 'false');
		}
		else
			animationFrameID = requestAnimationFrame(loop);

        topLeftPaddle.y += topLeftPaddle.dy;
        bottomLeftPaddle.y += bottomLeftPaddle.dy;
        topRightPaddle.y += topRightPaddle.dy;
        bottomRightPaddle.y += bottomRightPaddle.dy;
		
        // If the left paddle tries to go beyond the game field ,
        if (topLeftPaddle.y < grid) {
          // then keep it in place
          topLeftPaddle.y = grid;
        }
        // Check the same for bottom
        else if (topLeftPaddle.y > TopLeftmaxPaddleY) {
          topLeftPaddle.y = TopLeftmaxPaddleY;
        }
        if (bottomLeftPaddle.y < BottomLeftminPaddleY) 
          bottomLeftPaddle.y  = BottomLeftminPaddleY;
        else if (bottomLeftPaddle.y > BottomLeftmaxPaddleY) 
            bottomLeftPaddle.y = BottomLeftmaxPaddleY;

        // If the right paddle tries to go beyond the game field       

        if (topRightPaddle.y < grid) {
          topRightPaddle.y = grid;                              // then keep it in place
        }
        else if (topRightPaddle.y > TopRightmaxPaddleY) {       // Check the same for bottom
          topRightPaddle.y = TopRightmaxPaddleY;
        }
        if (bottomRightPaddle.y < BottomRightminPaddleY) 
            bottomRightPaddle.y = BottomRightminPaddleY;
        else if (bottomRightPaddle.y > BottomRightmaxPaddleY) 
            bottomRightPaddle.y = BottomRightmaxPaddleY;
       
        // Draw the paddles in white
        context.fillStyle = "white";
        // Each paddle is a rectangle
        context.fillRect(
          topLeftPaddle.x,
          topLeftPaddle.y,
          topLeftPaddle.width,
          topLeftPaddle.height
        );

        context.fillRect(
          bottomLeftPaddle.x,
          bottomLeftPaddle.y,
          bottomLeftPaddle.width,
          bottomLeftPaddle.height
        );
        
        context.fillRect(
          topRightPaddle.x,
          topRightPaddle.y,
          topRightPaddle.width,
          topRightPaddle.height
        );

        context.fillRect(
          bottomRightPaddle.x,
          bottomRightPaddle.y,
          bottomRightPaddle.width,
          bottomRightPaddle.height
        );

        // If the ball was moving on the previous step, let it continue moving
        ball.x += ball.dx;
        ball.y += ball.dy;
        // // If the ball touches the bottom wall, change its direction on the Y axis
        if (ball.y < grid) {
          ball.y = grid;
          ball.dy *= -1;
        }
        // Do the same if the ball touches the top wall
        else if (ball.y + grid > canvas.height - grid) {
          ball.y = canvas.height - grid * 2;
          ball.dy *= -1;
        }
        // If the ball goes off the game field to the left or right, restart it
        if ((ball.x < 0 || ball.x > canvas.width) && !ball.resetting) {
          // Mark that the ball is restarted to avoid looping
          ball.resetting = true;
		  if (ball.x < 0){
			right_score += 1;
		  }
		  else {
			left_score += 1;
		  }          
          
          setTimeout(() => {
            // Ball is back in the game
            ball.resetting = false;
            // Start it again from the center
            ball.x = canvas.width / 2;
            ball.y = canvas.height / 2;
          }, 1000);
        }
        // If the ball touches the left paddle,
        if (collides(ball, topLeftPaddle) || collides(ball, bottomLeftPaddle)) {
          // send it in the opposite direction
          ball.dx *= -1;
          if (collides(ball, topLeftPaddle))
            ball.x = topLeftPaddle.x + topLeftPaddle.width;
          else
            ball.x = bottomLeftPaddle.x + bottomLeftPaddle.width;         
        }
        // Check and do the same for the right paddle
        else if (collides(ball, topRightPaddle) || collides(ball, bottomRightPaddle)) {
          ball.dx *= -1;
          if (collides(ball, topRightPaddle))
            ball.x = topRightPaddle.x - ball.width;
          else
            ball.x = bottomRightPaddle.x - ball.width;
         
          // if it reaches 10 - activate the secret level
          if (left_score >= 5 || right_score >= 5) {
            secret = true;
          }
          // here's the secret level
          if (secret) {
            // increase new bounces
            secret_count += 1;
            // if this number is divisible by 3...
            if (secret_count % 3 == 0) {
              // increase the ball speed by one
              if (ball.dx > 0) {
                ball.dx += 1;
              } else {
                ball.dx -= 1;
              }
              if (ball.dy > 0) {
                ball.dy += 1;
              } else {
                ball.dy -= 1;
              }
              // randomly color the ball
              ballColor =
                "#" +
                (Math.random().toString(16) + "000000")
                  .substring(2, 8)
                  .toUpperCase();
            }
          }
        }
        // Draw the ball with the appropriate color
        context.fillStyle = ballColor;
        context.fillRect(ball.x, ball.y, ball.width, ball.height);
        // Draw the walls
        context.fillStyle = "white";
        context.fillRect(0, 0, canvas.width, grid);
        context.fillRect(0, canvas.height - grid, canvas.width, canvas.height);
        // Draw the grid in the middle
        for (let i = grid; i < canvas.height - grid; i += grid * 2) {
          context.fillRect(canvas.width / 2 - grid / 2, i, grid, grid);
        }
        // Track key presses
        
        
        document.addEventListener("keydown", function (e) {
            switch(e.which){
                case 87: // key 'w'
                    topLeftPaddle.dy = -paddleSpeed;
                    break;
                case 83: // key 's'
                    topLeftPaddle.dy = paddleSpeed;
                    break;
                case 84: // key 't'
                    bottomLeftPaddle.dy = -paddleSpeed;
                    break;
                case 71: // key 'g'
                    bottomLeftPaddle.dy = paddleSpeed;
                    break;
                case 73: // key 'i'
                    topRightPaddle.dy = -paddleSpeed;
                    break;
                case 75: // key 'k'
                    topRightPaddle.dy = paddleSpeed;
                    break;
                case 38: // key 'up'
                    bottomRightPaddle.dy = -paddleSpeed;
                    break;
                case 40: // key 'down'
                    bottomRightPaddle.dy = paddleSpeed;
                    break;
            }
        });   

      // And now, listen for when someone releases a key to stop the paddle's movement
        document.addEventListener("keyup", function (e) {
        // If it's the up or down arrow or 'w' or 's',
            if (e.which === 87 || e.which === 83) {
                // stop the right paddle
                topLeftPaddle.dy = 0;
            }
            else if (e.which === 71 || e.which === 84) {
                bottomLeftPaddle.dy = 0;
            }
            else if (e.which === 73 || e.which === 75) {
                topRightPaddle.dy = 0;
            }
            else if (e.which === 38 || e.which === 40) {
                bottomRightPaddle.dy = 0;
            }
        });
        // Track mouse movements  
        // Text color
        context.fillStyle = "#ff00ff";
        // Set the size and font
        context.font = "bold 20pt Courier";
        // First, display the record
        context.fillText(left_score, canvas.width /4, 50);
        context.fillText(right_score, canvas.width *3/4, 50);
      }
      // Start the game
      requestAnimationFrame(loop);
    };

	
	function stopGame() {
		// Add any additional cleanup logic or actions you need
		gameRunning = false;
	}

	window.addEventListener('beforeunload', function() {
		localStorage.setItem('gamesFlag', 'false');
	  });

	  window.addEventListener("popstate", function () {
		localStorage.setItem('gamesFlag', 'false');
		stopGame();

	  });
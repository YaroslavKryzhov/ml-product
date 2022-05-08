import {
  AppBar,
  Checkbox,
  Chip,
  FormControlLabel,
  Paper,
  Stack,
  TextField,
  Toolbar,
} from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import React, { useCallback, useEffect, useState } from "react";
import { CenteredContainer, helperTextProps } from "components/muiOverride";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import {
  changeAuthPage,
  changeEmail,
  changePasswordInput,
  changeSecondPasswordInput,
} from "ducks/reducers/auth";
import { AppPage, AuthPage } from "ducks/reducers/types";
import EmailValidator from "email-validator";
import {
  useAuthMutation,
  useRegisterMutation,
} from "ducks/reducers/api/auth.api";
import { theme } from "globalStyle/theme";
import { PASSWORD_ERROR } from "./const";
import { passwordValidate } from "./helpers";
import { useNavigate } from "react-router-dom";

export const Authentication: React.FC = () => {
  const { passwordInput, emailInput, page, secondPasswordInput } =
    useSESelector((state) => state.auth);
  const dispatch = useAppDispatch();
  const [isFirstTry, setIsFirstTry] = useState(true);
  const navigate = useNavigate();
  const [register, { isLoading: isRegLoading }] = useRegisterMutation();
  const [
    auth,
    { isLoading: isAuthLoading, isSuccess: isAuthSuccess, data: authResponse },
  ] = useAuthMutation();
  const isLoading = isRegLoading || isAuthLoading;

  const isEmailError = !EmailValidator.validate(emailInput);
  const isPasswordError =
    (page === AuthPage.register && !passwordInput) ||
    !passwordValidate(passwordInput);
  const isSecondPasswordError =
    page === AuthPage.register &&
    (!secondPasswordInput ||
      !passwordValidate(secondPasswordInput) ||
      secondPasswordInput !== passwordInput);

  const authCallback = useCallback(() => {
    setIsFirstTry(false);
    if (isEmailError || isPasswordError || isSecondPasswordError) return;

    if (page === AuthPage.auth)
      auth({ username: emailInput, password: passwordInput });
    else register({ email: emailInput, password: passwordInput });
  }, [
    auth,
    register,
    page,
    isEmailError,
    isPasswordError,
    isSecondPasswordError,
    emailInput,
    passwordInput,
  ]);

  useEffect(() => setIsFirstTry(true), [page]);

  useEffect(() => {
    if (isAuthSuccess) {
      localStorage.authToken = authResponse?.access_token;

      navigate(`/${AppPage.Workplace}`);
    }
  }, [isAuthSuccess, authResponse]);

  return (
    <Stack direction="column" sx={{ height: "100vh" }}>
      <AppBar position="static">
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <Chip
            sx={{
              backgroundColor: "primary.light",
              color: "primary.contrastText",
              "&:hover": {
                backgroundColor: "secondary.dark",
              },
            }}
            clickable
            onClick={() => {
              dispatch(
                page === AuthPage.auth
                  ? changeAuthPage(AuthPage.register)
                  : changeAuthPage(AuthPage.auth)
              );
              setIsFirstTry(true);
            }}
            label={page === AuthPage.auth ? "Регистрация" : "Авторизация"}
          />
        </Toolbar>
      </AppBar>
      <CenteredContainer sx={{ flexGrow: 1 }}>
        <Paper sx={{ width: 657, p: theme.spacing(4) }} elevation={3}>
          <Stack direction="column">
            <TextField
              size="small"
              type="email"
              label="Почта"
              value={emailInput}
              error={!isFirstTry && isEmailError}
              helperText={!isFirstTry && isEmailError ? "Неверная почта" : " "}
              onChange={(e) => dispatch(changeEmail(e.target.value))}
              FormHelperTextProps={helperTextProps}
              sx={{ mb: theme.spacing(2) }}
            />
            <TextField
              size="small"
              type="password"
              label="Пароль"
              value={passwordInput}
              onChange={(e) => dispatch(changePasswordInput(e.target.value))}
              helperText={!isFirstTry && isPasswordError ? PASSWORD_ERROR : " "}
              error={!isFirstTry && isPasswordError}
              FormHelperTextProps={helperTextProps}
              sx={{ mb: theme.spacing(2) }}
            />
            {page === AuthPage.register && (
              <TextField
                size="small"
                type="password"
                label="Повторите пароль"
                value={secondPasswordInput}
                FormHelperTextProps={helperTextProps}
                onChange={(e) =>
                  dispatch(changeSecondPasswordInput(e.target.value))
                }
                sx={{ mb: theme.spacing(2) }}
                error={!isFirstTry && isSecondPasswordError}
                helperText={
                  !isFirstTry && isSecondPasswordError
                    ? secondPasswordInput !== passwordInput
                      ? "Пароли не совпадают"
                      : PASSWORD_ERROR
                    : " "
                }
              />
            )}
            {page === AuthPage.auth && (
              <FormControlLabel
                control={<Checkbox size="small" />}
                label="Запомнить меня"
                sx={{ mt: theme.spacing(4) }}
              />
            )}
            <LoadingButton
              loading={isLoading}
              size="small"
              variant="contained"
              onClick={authCallback}
              sx={{
                mt: theme.spacing(2),
              }}
            >
              {page === AuthPage.auth ? "Войти" : "Зарегистрироваться"}
            </LoadingButton>
          </Stack>
        </Paper>
      </CenteredContainer>
    </Stack>
  );
};
